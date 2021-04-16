import torch
import numpy as np

import skimage.io
import skimage.transform
import yaml
import sys
import numpy as np
import cv2
import os

import model
import json
from dataloader import UnNormalizer

def preprocesss(image):
    image = normalizer(image)
    image = resizer(image)
    return image

def normalizer(image):
    mean = np.array([[[0.485, 0.456, 0.406]]])
    std = np.array([[[0.229, 0.224, 0.225]]])

    return ((image.astype(np.float32) - mean) / std)

def resizer(image):
    min_side = 600
    max_side = 720

    rows, cols, cns = image.shape
    #print("before: rows-{}, cols-{}, channels-{}".format(rows, cols, cns))

    smallest_side = min(rows, cols)
    scale = min_side / smallest_side

    largest_side = max(rows, cols)
    if largest_side * scale > max_side:
        scale =  max_side / largest_side
    
    image = skimage.transform.resize(
        image, (int(round(rows * scale)), int(round(cols*scale)))
    )
    rows, cols, cns = image.shape
    #print("after: rows-{}, cols-{}, channels-{}".format(rows, cols, cns))

    pad_w = 32 - rows % 32
    pad_h = 32 - cols % 32
    #print(pad_w, ",", pad_h)
    #print(rows-pad_w, cols-pad_h)

    new_image = np.zeros((rows + pad_w, cols + pad_h, cns)).astype(np.float32)
    new_image[:rows, :cols, :] = image.astype(np.float32)
    rows, cols, cns = new_image.shape
    #print("final: rows-{}, cols-{}, channels-{}".format(rows, cols, cns))
    image_tensor = torch.from_numpy(new_image)
    return image_tensor

def draw_caption(image, box, caption):
    b = np.array(box).astype(int)
    cv2.putText(image, caption, (b[0], b[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 2)
    cv2.putText(image, caption, (b[0], b[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

def inference(image, model, device, threshold=0.05):
    unnormalizer = UnNormalizer()
    model.eval()
    
    with torch.no_grad():
        image = image.permute(2,0,1)
        scores, labels, boxes = model(image.to(device).float().unsqueeze(dim=0))
        scores = scores.cpu()
        labels = labels.cpu()
        boxes = boxes.cpu()

        idxs = np.where(scores > 0.5)
        image = unnormalizer(image)
        image = np.array(255 * image).copy()

        image[image < 0] = 0
        image[image > 255] = 255

        image = np.transpose(image, (1,2,0))
        image = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2RGB)

        for i in range(idxs[0].shape[0]):
            score = scores.cpu().numpy()[i]
            bbox = boxes[idxs[0][i], :]
            x1 = int(bbox[0])
            y1 = int(bbox[1])
            x2 = int(bbox[2])
            y2 = int(bbox[3])
            caption = "pred:({:.2f})".format(score)
            draw_caption(image, (x1, y1, x2, y2), caption)
            cv2.rectangle(image, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
        return image


def main():
    configuration_path = 'configuration.yml'

    with open(configuration_path, 'r') as cfg_path:
        cfg = yaml.safe_load(cfg_path)
    
    val_json = cfg['validation']['annotation']
    json_file = open(val_json, 'rt', encoding='UTF-8') 
    coco = json.load(json_file)
    
    categories = coco['categories']
    num_classes = len(categories)

    img_path = sys.argv[1]
    
    img = skimage.io.imread(img_path)
    img = img.astype(np.float32) / 255.0

    model_path = os.path.join(cfg['result']['result_dir'], "best_model.pt")
    
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
    model_ft.load_state_dict(torch.load(model_path))

    model_ft.training=False
    model_ft.eval()
    model_ft.freeze_bn()

    img_tensor = preprocesss(img)
    result = inference(img_tensor, model_ft, device, threshold=0.01)
    result_path = os.path.join(cfg['result']['result_dir'], "result.jpg")
    cv2.imwrite(result_path, result)

if __name__ == "__main__":
    main()