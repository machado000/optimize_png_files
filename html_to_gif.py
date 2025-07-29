import imageio.v2 as imageio
import time
import os
import subprocess

from pathlib import Path
from PIL import Image
from selenium import webdriver


project_path = Path(__file__).parent.resolve()
source_path = "I:\\Meu Drive\\02 - MATERIAIS\\024_NACIONAL RIO_CMRJ_CAMERA APROVA\\nacional_cmrj_cidadania_v4"
destination_path = "I:\\Meu Drive\\02 - MATERIAIS\\024_NACIONAL RIO_CMRJ_CAMERA APROVA\\nacional_cmrj_cidadania_gifs"
gifsicle_path = os.path.join(project_path, "gifsicle", "gifsicle.exe")

temp_path = os.path.join(project_path, "temp")
os.makedirs(temp_path, exist_ok=True)


banner_list = [
    "banner_1_300x250",
    "banner_1_300x600",
    "banner_1_160x600",
    "banner_1_728x90",
    "banner_1_970x90",
    "banner_1_468x60",
    "banner_1_970x150",
    "banner_1_970x250",
    "banner_1_1040x210",
    "banner_1_300x100",
    "banner_1_320x150",
    "banner_1_320x100",
    "banner_1_336x280",
    "banner_1_250x250",
    "banner_1_200x200",
    "banner_1_320x50",
    "banner_1_300x50",
]

banner_sizes = {
    "banner_1_300x250": (300, 250, 12),
    "banner_1_300x600": (300, 600, 12),
    "banner_1_160x600": (160, 600, 12),
    "banner_1_728x90": (728, 90, 12),
    "banner_1_970x90": (970, 90, 12),
    "banner_1_468x60": (468, 60, 12),
    "banner_1_970x150": (970, 150, 12),
    "banner_1_970x250": (970, 250, 12),
    "banner_1_1040x210": (1040, 210, 12),
    "banner_1_300x100": (300, 100, 12),
    "banner_1_320x150": (320, 150, 12),
    "banner_1_320x100": (320, 100, 12),
    "banner_1_336x280": (336, 280, 12),
    "banner_1_250x250": (250, 250, 12),
    "banner_1_200x200": (200, 200, 12),
    "banner_1_320x50": (320, 50, 12),
    "banner_1_300x50": (300, 50, 12),
}


driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)

for banner in banner_list:

    banner_path = os.path.join(source_path, banner, "index.html")
    width, height, gif_duration_seconds = banner_sizes.get(banner, (300, 250, 15))

    gif_fps = 3
    frame_count = gif_duration_seconds * gif_fps
    frame_duration = 1 / gif_fps

    driver.get(f"file:///{banner_path}")  # Local HTML banner

    frames = []
    frames_paths = []

    for i in range(frame_count):
        time.sleep(frame_duration)  # wait for animation
        frame = os.path.join(project_path, "temp", f"frame_{i}.png")
        driver.save_screenshot(frame)

        # Crop from top left
        with Image.open(frame) as img:
            cropped = img.crop((0, 0, width, height))
            cropped = cropped.convert("P", palette=Image.ADAPTIVE, colors=256)
            cropped.save(frame, optimize=True)

        frames.append(imageio.imread(frame))
        frames_paths.append(frame)

    # Save as GIF
    gif_path = os.path.join(destination_path, f"{banner}.gif")
    imageio.mimsave(gif_path, frames, format='GIF', duration=int(frame_duration * 2000), loop=0, subrectangles=True)

    # # Optimize GIF with pygifsicle
    # optimized_gif_path = os.path.join(destination_path, f"{banner}.gif")
    # subprocess.run([
    #     gifsicle_path,
    #     "-b",
    #     "--optimize=3",
    #     "--colors=256",
    #     "--lossy=100",
    #     gif_path,
    #     "-o", optimized_gif_path,
    # ], check=True)

    # Clean up
    for f in frames_paths:
        os.remove(f)

driver.quit()
