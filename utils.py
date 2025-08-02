import os
import uuid
import torch
from langdetect import detect
from keybert import KeyBERT
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline

# Load Whisper model
asr = pipeline("automatic-speech-recognition", model="openai/whisper-small")

# Keyword extraction
kw_model = KeyBERT()

def transcribe_audio(audio_path):
    result = asr(audio_path)
    return result['text']

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def extract_keywords(text, num_keywords=5):
    keywords = kw_model.extract_keywords(text, top_n=num_keywords)
    return [kw[0] for kw in keywords]

def create_story_tile(text, keywords, bg_image='assets/default_bg.jpg', output_dir='tiles'):
    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(bg_image).convert("RGB")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", size=28)
    except:
        font = ImageFont.load_default()

    width, height = img.size
    margin = 50
    lines = []
    words = text.split(' ')
    line = ""

    for word in words:
        test_line = line + word + " "
        if draw.textlength(test_line, font=font) < (width - 2 * margin):
            line = test_line
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    y_text = margin
    for line in lines:
        draw.text((margin, y_text), line, font=font, fill="black")
        y_text += 35

    # Add keywords at the bottom
    kw_text = "Keywords: " + ", ".join(keywords)
    draw.text((margin, height - 50), kw_text, font=font, fill="gray")

    filename = f"{output_dir}/story_{uuid.uuid4().hex[:6]}.jpg"
    img.save(filename)
    return filename
