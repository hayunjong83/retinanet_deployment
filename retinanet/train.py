import numpy as np
import os
import sys
import json
import yaml

import torch
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import DataLoader, random_split
from dataloader import CustomDataset, collater, Resizer, AspectRatioBasedSampler, Augmenter, Normalizer

import model
from tqdm import tqdm

def main():
    configuration_path = 'configuration.yml'
    if not os.path.isfile(configuration_path):
        print("There's no configuraion file. Please Check it!")
        return
    
    with open(configuration_path, 'r') as cfg_path:
        cfg = yaml.safe_load(cfg_path)

    train_dir = cfg['train']['image_dir']
    train_json = cfg['train']['annotation']

    transform = transforms.Compose([
        Normalizer(), Augmenter(), Resizer()])
    train_dataset = CustomDataset(train_dir, train_json, transform)
    num_classes = train_dataset.num_classes

    batch_size = cfg['train']['batch_size']
    train_sampler = AspectRatioBasedSampler(train_dataset, batch_size=batch_size, drop_last=False)
    train_dataloader = DataLoader(train_dataset, num_workers=4, collate_fn=collater, batch_sampler=train_sampler)

    val_dir = cfg['validation']['image_dir']
    val_json = cfg['validation']['annotation']

    val_dataset = CustomDataset(val_dir, val_json, transform)
    batch_size = cfg['validation']['batch_size']
    val_sampler = AspectRatioBasedSampler(val_dataset, batch_size=batch_size, drop_last=False)
    val_dataloader = DataLoader(val_dataset, num_workers=4, collate_fn=collater, batch_sampler=val_sampler)

    model_name = cfg['train']['model']
    if model_name == "resnet18":
        model_ft = model.resnet18(num_classes=num_classes, pretrained=True)
    elif model_name == "resnet34":
        model_ft = model.resnet34(num_classes=num_classes, pretrained=True)
    elif model_name == "resnet50":
        model_ft = model.resnet50(num_classes=num_classes, pretrained=True)
    elif model_name == "resnet101":
        model_ft = model.resnet101(num_classes=num_classes, pretrained=True)
    else:
        raise ValueError('Unsupported model name')
    
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model_ft = model_ft.to(device)

    optimizer = optim.Adam(model_ft.parameters(), lr=1e-5)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3, verbose=True)

    num_epochs = cfg['train']['epochs']
    num_train_batch = len(train_dataloader)
    num_val_batch = len(val_dataloader)

    best_loss = 1000000
    result_path = cfg['result']['result_dir']
    if not os.path.isdir(result_path):
        os.makedirs(result_path, exist_ok=True)

    for epoch in range(num_epochs):
        model_ft.train()

        optimizer.zero_grad()
        train_classification_loss = 0.0
        train_regression_loss = 0.0
        epoch_loss = []
        
        for i, sample in enumerate(tqdm(train_dataloader)):
            optimizer.zero_grad()

            classification_loss, regression_loss = model_ft(
                [sample["img"].to(device).float(), sample["annot"].to(device)])

            classification_loss = classification_loss.mean()
            regression_loss = regression_loss.mean()
            loss = classification_loss + regression_loss
            loss.backward()

            torch.nn.utils.clip_grad_norm_(model_ft.parameters(), 0.1)

            optimizer.step()

            train_classification_loss += classification_loss
            train_regression_loss += regression_loss

            del classification_loss
            del regression_loss
            epoch_loss.append(float(loss))
        
        train_classification_loss /= num_train_batch
        train_regression_loss /= num_train_batch
        print('Train Epoch {}/{} : classification loss: {:1.5f}, regression loss: {:1.5f}'.format(
            epoch + 1, num_epochs, train_classification_loss, train_regression_loss
        ))

        with torch.no_grad():
            val_classification_loss = 0.0
            val_regression_loss = 0.0
            print(device)
            for i, sample in enumerate(tqdm(val_dataloader)):
                
                classification_loss, regression_loss = model_ft(
                    [sample['img'].to(device).float(), sample['annot'].to(device)])
                
                classification_loss = classification_loss.mean()
                regression_loss = regression_loss.mean()
                val_loss = classification_loss + regression_loss

                val_classification_loss += classification_loss
                val_regression_loss += regression_loss

                del classification_loss
                del regression_loss
            
            val_classification_loss /= num_val_batch
            val_regression_loss /= num_val_batch
            val_loss = val_classification_loss + val_regression_loss
            print('Validation Epoch {}/{} : classification loss: {:1.5f}, regression loss: {:1.5f}'.format(
                epoch + 1, num_epochs, val_classification_loss, val_regression_loss
            ))
        
        scheduler.step(np.mean(epoch_loss))

        if val_loss < best_loss:
            best_loss = val_loss
            torch.save(model_ft.state_dict(), os.path.join(result_path, 'best_model.pt'))

if __name__ == '__main__':
    main()