import moviepy as mp
import os

from pathlib import Path


project_path = Path(__file__).parent.resolve()
source_path = "I:\\Meu Drive\\02 - MATERIAIS\\024_NACIONAL RIO_CMRJ_CAMERA APROVA\\nacional_cmrj_cidadania_v5"
destination_path = "I:\\Meu Drive\\02 - MATERIAIS\\024_NACIONAL RIO_CMRJ_CAMERA APROVA\\nacional_cmrj_cidadania_gifs_2"
# gifsicle_path = os.path.join(project_path, "gifsicle", "gifsicle.exe")

os.makedirs(destination_path, exist_ok=True)

subfolders = [f.name for f in Path(source_path).iterdir() if f.is_dir()]

for subfolder in subfolders:

    subfolder_path = os.path.join(source_path, subfolder)
    output_path = os.path.join(destination_path, f"{subfolder}.gif")

    # Config
    image_files = [os.path.join(subfolder_path, f"{i:02}.png") for i in range(1, 10)]
    timestamps = [0, 0.3, 0.6, 4, 4.3, 4.6, 9, 9.3, 9.6]  # when each image appears (in seconds)
    duration = 12

    # Create base empty clip
    clips = []
    for i, img_path in enumerate(image_files):
        clip = mp.ImageClip(img_path).with_start(timestamps[i]).with_duration(duration - timestamps[i])
        clips.append(clip)

    final = mp.CompositeVideoClip(clips, size=clips[0].size).with_duration(duration)
    final.write_gif(output_path, fps=10)

    # # Optimize GIF with pygifsicle
    # optimized_gif_path = os.path.join(destination_path, f"{subfolder}_otimized.gif")
    # subprocess.run([
    #     gifsicle_path,
    #     "-b",
    #     "--optimize=3",
    #     "--colors=256",
    #     "--lossy=100",
    #     gif_path,
    #     "-o", optimized_gif_path,
    # ], check=True)
