import os
import random
import subprocess
import textwrap
from datetime import date
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

FACTS = [
    ("INDIA FACTS", "India has one of the world's largest railway networks."),
    ("SPACE FACTS", "The Moon takes about 27 days to orbit Earth."),
    ("SCIENCE FACTS", "Light travels faster than sound."),
    ("ANIMAL FACTS", "Octopuses have three hearts."),
    ("OCEAN FACTS", "Most of Earth's surface is covered by water."),
    ("HISTORY FACTS", "Paper-making developed in ancient China."),
    ("TECH FACTS", "The first website went online in 1991."),
]

# Stable daily choice; change the list to use your own reviewed, original scripts.
title, fact = FACTS[date.today().timetuple().tm_yday % len(FACTS)]
narration = f"{title}. {fact} Follow for more."

def load_font(size, bold=True):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()

W, H = 1080, 1920
img = Image.new("RGB", (W, H), (15, 25, 55))
draw = ImageDraw.Draw(img)
# Simple decorative shapes
draw.rounded_rectangle((45, 260, 1035, 1660), radius=48, fill=(26, 43, 83), outline=(83, 150, 240), width=5)
title_font = load_font(72)
body_font = load_font(62)
footer_font = load_font(42)

draw.text((80, 380), title, font=title_font, fill=(255, 220, 70))
wrapped = textwrap.wrap(fact, width=23)
y = 650
for line in wrapped:
    draw.text((80, y), line, font=body_font, fill="white")
    y += 100
draw.text((80, 1450), "FOLLOW FOR MORE", font=footer_font, fill=(255, 220, 70))
image_path = OUT / "short.png"
img.save(image_path)

def run(cmd):
    subprocess.run(cmd, check=True)

# GitHub Actions installs espeak and ffmpeg. Local runs need them installed too.
audio_path = OUT / "voice.wav"
run(["espeak", "-s", "145", "-w", str(audio_path), narration])

video_path = OUT / "short.mp4"
run([
    "ffmpeg", "-y", "-loop", "1", "-i", str(image_path), "-i", str(audio_path),
    "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "128k",
    "-pix_fmt", "yuv420p", "-shortest", "-vf", "scale=1080:1920",
    "-movflags", "+faststart", str(video_path)
])

print(f"Created {video_path}")
if os.environ.get("YOUTUBE_UPLOAD_ENABLED", "false").lower() == "true":
    from src.upload_youtube import upload_video
    upload_video(video_path, title=f"{title}: {fact[:65]}", description="Daily short. Check facts and rights before publishing.", privacy="private")
else:
    print("Upload disabled; download the workflow artifact to review the video.")
