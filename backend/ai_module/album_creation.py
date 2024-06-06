import os
import uuid
from fpdf import FPDF
from .image_processing import analyze_images, classify_images
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)

def convert_jfif_to_jpeg(image_path):
    if image_path.lower().endswith('.jfif'):
        try:
            img = Image.open(image_path)
            new_image_path = image_path.rsplit('.', 1)[0] + '.jpg'
            img.save(new_image_path, 'JPEG')
            logging.info(f"Converted {image_path} to {new_image_path}")
            return new_image_path
        except Exception as e:
            logging.error(f"Error converting image {image_path}: {e}")
    return image_path

def create_photo_albums(image_paths, album_folder):
    analysis_results = analyze_images(image_paths)
    n_clusters = max(2, len(image_paths) // 2)
    classifications = classify_images(analysis_results, n_clusters)

    albums = {}
    for image_path, label in zip(image_paths, classifications):
        label = str(label)
        if label not in albums:
            albums[label] = []
        albums[label].append(image_path)

    album_paths = []
    for label, images in albums.items():
        try:
            album_filename = f"{label}_album_{uuid.uuid4().hex}.pdf"
            album_path = os.path.join(album_folder, album_filename)

            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=16)

            # Add cover page with album title and first photo
            pdf.add_page()
            pdf.set_font("Arial", size=28, style='B')
            pdf.cell(0, 10, f"{label.capitalize()} Album", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=16)

            if images:
                converted_image_path = convert_jfif_to_jpeg(images[0])
                pdf.image(converted_image_path, x=10, y=30, w=190, h=240)
                pdf.set_line_width(1)
                pdf.rect(10, 30, 190, 240)
                pdf.ln(275)

            # Add remaining photos
            for image_path in images[1:]:
                pdf.add_page()
                converted_image_path = convert_jfif_to_jpeg(image_path)
                pdf.image(converted_image_path, x=10, y=10, w=190, h=270)
                pdf.set_line_width(1)
                pdf.rect(10, 10, 190, 270)

            pdf.output(album_path)
            album_paths.append(album_path)
            logging.info(f"Created album: {album_path}")
        except Exception as e:
            logging.error(f"Error creating album for label {label}: {e}")

    return album_paths
