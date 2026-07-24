import os
import uuid
from langdetect import detect
from keybert import KeyBERT
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline

# Load Whisper model with forced English transcription
asr = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small",
    tokenizer="openai/whisper-small"
)

# Keyword extraction
kw_model = KeyBERT()

def transcribe_audio(audio_path):
    try:
        result = asr(audio_path, generate_kwargs={"task": "transcribe", "language": "en"})
        text = result['text'].strip()

        # Very short or repeated outputs likely bad
        if len(text) < 5 or text.lower().count(text.split()[0]) > 10:
            return "Transcription unclear"
        return text
    except Exception as e:
        return f"[Error in transcription] {e}"

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def extract_keywords(text, num_keywords=5):
    try:
        keywords = kw_model.extract_keywords(text, top_n=num_keywords)
        return [kw[0] for kw in keywords]
    except:
        return []

# Summarization model (loaded lazily to optimize application startup)
summarizer = None

def get_summarizer():
    global summarizer
    if summarizer is None:
        summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6"
        )
    return summarizer

def summarize_text(text):
    words = text.split()
    lang = detect_language(text)
    
    # If the text is short or not English, return the original text since distilbart is English-only.
    if len(words) < 30 or lang != "en":
        return text
        
    try:
        summarizer_pipeline = get_summarizer()
        input_len = len(words)
        max_len = min(75, max(15, int(input_len * 0.6)))
        min_len = min(15, int(max_len * 0.4))
        
        result = summarizer_pipeline(text, max_length=max_len, min_length=min_len, do_sample=False)
        return result[0]['summary_text'].strip()
    except Exception as e:
        return f"[Error in summarization] {e}"

def create_story_tile(text, keywords, bg_image='assets/default_bg.jpg', output_dir='tiles'):
    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(bg_image).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Try loading Noto font first
    try:
        font = ImageFont.truetype("assets/NotoSans-Regular.ttf", size=28)
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

    # Add keywords at bottom
    kw_text = "Keywords: " + ", ".join(keywords)
    draw.text((margin, height - 50), kw_text, font=font, fill="gray")

    filename = f"{output_dir}/story_{uuid.uuid4().hex[:6]}.jpg"
    img.save(filename)
    return filename
