import io
import json
import torch
from torchvision import models, transforms
from PIL import Image

imagenet_class_index = json.load(open('imagenet_class_index.json'))
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = models.densenet121(pretrained=True)
model = model.to(device)

model.eval()

def transform_image(image_bytes):
    image_transforms = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return image_transforms(image).unsqueeze(0)

def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes).to(device)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]

def batch_prediction(image_bytes_batch):
    image_tensors = [transform_image(image_bytes=image_bytes) for image_bytes in image_bytes_batch]
    tensor = torch.cat(image_tensors).to(device)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_ids = y_hat.tolist()
    return [imagenet_class_index[str(i)] for i in predicted_ids]