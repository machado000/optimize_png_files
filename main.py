import os
from PIL import Image
import tinify
from tqdm import tqdm


tinify.key = "P8mMyqmnH3Nd6BV8KWR2Z8YC8DHwxk6Q"


# Function to optimize PNG using Pillow
def optimize_png(image_path):
    with Image.open(image_path) as img:
        # Convert image to 'RGBA' (if it isn't already) and optimize
        img = img.convert("RGBA")
        img.save(image_path, format="PNG", optimize=True, quality=85)

# Function to optimize all PNGs in a directory using Pillow with size check


def optimize_pngs_in_directory(directory, size_threshold_kb=100):
    optimized_count = 0
    all_png_files = []

    # Collecting all PNG files above the size threshold
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                file_path = os.path.join(root, file)
                if os.stat(file_path).st_size > size_threshold_kb * 1024:
                    all_png_files.append(file_path)

    # Iterating with tqdm progress bar
    for file_path in tqdm(all_png_files, desc="Optimizing PNGs", unit="file"):
        optimize_png(file_path)
        optimized_count += 1

    print(f"\nTotal optimized PNG files: {optimized_count}")

# Function to tinify PNG using tinify API


def tinify_png(image_path):
    source = tinify.from_file(image_path)
    source.to_file(image_path)

# Function to tinify all PNGs in a directory with size check


def tinify_pngs_in_directory(directory, size_threshold_kb=100):
    tinified_count = 0
    all_png_files = []

    # Collecting all PNG files above the size threshold
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.png'):
                file_path = os.path.join(root, file)
                if os.stat(file_path).st_size > size_threshold_kb * 1024:
                    all_png_files.append(file_path)

    # Iterating with tqdm progress bar
    for file_path in tqdm(all_png_files, desc="Tinifying PNGs", unit="file"):
        tinify_png(file_path)
        tinified_count += 1

    print(f"\nTotal tinified PNG files: {tinified_count}")


# Provide the starting directory
starting_directory = "H:\\Meu Drive\\02 - MATERIAIS\\062_PROPEG_SECOM_CONHECA_O_BRASIL\\pacotes completos"

# Running the tinify function
tinify_pngs_in_directory(starting_directory)
