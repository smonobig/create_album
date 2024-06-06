import torch
from torchvision import models, transforms
from PIL import Image

def load_model():
    model = models.resnet50(pretrained=True)
    model.eval()
    return model

def preprocess_image(image_path):
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path).convert("RGB")
    image_tensor = preprocess(image).unsqueeze(0)
    return image_tensor

def analyze_image(image_tensor, model):
    with torch.no_grad():
        output = model(image_tensor)
    return output
