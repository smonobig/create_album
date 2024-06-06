import torch
from torchvision import models, transforms
from PIL import Image
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import logging

logging.basicConfig(level=logging.INFO)

def analyze_images(image_paths):
    model = models.resnet50(weights='ResNet50_Weights.DEFAULT')
    model.eval()

    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    features = []

    with torch.no_grad():
        for image_path in image_paths:
            try:
                image = Image.open(image_path).convert("RGB")
                input_tensor = preprocess(image)
                input_batch = input_tensor.unsqueeze(0)
                output = model(input_batch)
                features.append(output.numpy().flatten())
                logging.info(f"Processed {image_path}")
            except Exception as e:
                logging.error(f"Error processing image {image_path}: {e}")

    return np.array(features)

def classify_images(features, n_clusters):
    n_samples, n_features = features.shape
    n_components = min(n_samples, n_features) // 2

    logging.info(f"Running PCA with n_components={n_components}")

    pca = PCA(n_components=n_components)
    reduced_features = pca.fit_transform(features)

    logging.info(f"Reduced features shape: {reduced_features.shape}")

    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(reduced_features)

    logging.info(f"Generated labels: {labels}")

    return labels
