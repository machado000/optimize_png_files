import os
import tinify

from PIL import Image
from tqdm import tqdm

from dotenv import load_dotenv
load_dotenv()


def main() -> None:

    # Load Tinify API key from enviroment
    tinify.key = os.getenv("TINIFY_KEY")

    # Provide the starting directory
    starting_directory = "H:\\Meu Drive\\02 - MATERIAIS\\068_NOVA_SECOM_BALANÇO\\secom_balanco_linha_3"

    # Running the tinify function
    tinify_pngs_in_directory(starting_directory, size_threshold_kb=50)


def optimize_png(image_path):
    # Function to optimize PNG using Pillow
    with Image.open(image_path) as img:
        # Convert image to 'RGBA' (if it isn't already) and optimize
        img = img.convert("RGBA")
        img.save(image_path, format="PNG", optimize=True, quality=85)


def optimize_pngs_in_directory(directory, size_threshold_kb=100):
    # Function to optimize all PNGs in a directory using Pillow with size check
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


def tinify_png(image_path):
    # Function to tinify PNG using tinify API
    source = tinify.from_file(image_path)
    source.to_file(image_path)


def tinify_pngs_in_directory(directory, size_threshold_kb=100):
    # Function to tinify all PNGs in a directory with size check
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
        file_size = os.stat(file_path).st_size
        print(f"Optimizing file '{file_path}' - {file_size}")
        tinify_png(file_path)
        tinified_count += 1

    print(f"\nTotal tinified PNG files: {tinified_count}")


if __name__ == "__main__":
    main()
