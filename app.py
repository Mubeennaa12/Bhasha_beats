import streamlit as st
import os
import pandas as pd
from utils import transcribe_audio, detect_language, extract_keywords, create_story_tile
import datetime

# Paths
DATA_FILE = "data/stories.csv"
os.makedirs("data", exist_ok=True)

# Load or initialize data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["timestamp", "text", "language", "keywords", "image_path"])

# --- 🌈 Custom Styling ---
st.set_page_config(page_title="BhashaBeat", layout="centered")
st.markdown("""
    <style>
    .stApp {
        background-color: #f3f0ec;
        background-image: url('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=1500&q=80');
        background-size: cover;
        background-attachment: fixed;
    }
    h1 {
        text-align: center;
        color: #4B0082;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #444;
        margin-bottom: 40px;
    }
    .footer {
        text-align: center;
        font-size: 13px;
        color: gray;
        padding-top: 2em;
    }
    </style>
""", unsafe_allow_html=True)

# --- 🧠 Title ---
st.markdown("<h1>🎙️ BhashaBeat</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Preserve the voice of India – one story at a time.</div>", unsafe_allow_html=True)

# --- 🧾 Tabs for Input ---
tab1, tab2 = st.tabs(["🗣️ Record Voice", "⌨️ Enter Text"])

with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_audio = st.file_uploader("Upload your voice (.wav/.mp3)", type=["wav", "mp3"])
    with col2:
        st.markdown("🎧 Listen back here")

    if uploaded_audio:
        st.audio(uploaded_audio)

        with st.expander("ℹ️ What happens next?"):
            st.write("Your voice is transcribed using Whisper, keywords extracted with KeyBERT, and a story tile is generated.")

        if st.button("Transcribe & Save"):
            with st.spinner("Processing your story..."):
                temp_path = f"temp_{uploaded_audio.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_audio.read())

                text = transcribe_audio(temp_path)
                lang = detect_language(text)
                keywords = extract_keywords(text)
                image_path = create_story_tile(text, keywords)

                timestamp = datetime.datetime.now().isoformat()
                df.loc[len(df)] = [timestamp, text, lang, ",".join(keywords), image_path]
                df.to_csv(DATA_FILE, index=False)

                st.success("✅ Story added!")
                st.image(image_path, caption="🖼️ Your Story Tile", use_column_width=True)
                os.remove(temp_path)

with tab2:
    text_input = st.text_area("✍️ Type your story, idiom, or proverb here")

    if st.button("Save Text Story"):
        if text_input.strip() == "":
            st.warning("⚠️ Please enter some text before saving.")
        else:
            lang = detect_language(text_input)
            keywords = extract_keywords(text_input)
            image_path = create_story_tile(text_input, keywords)

            timestamp = datetime.datetime.now().isoformat()
            df.loc[len(df)] = [timestamp, text_input, lang, ",".join(keywords), image_path]
            df.to_csv(DATA_FILE, index=False)

            st.success("✅ Story added!")
            st.image(image_path, caption="🖼️ Your Story Tile", use_column_width=True)

# --- 🪟 Display Submitted Stories ---
st.markdown("---")
st.subheader("📚 Stories You've Shared")

if len(df):
    for i in reversed(df.index):
        story = df.loc[i]
        st.image(story["image_path"], caption=f"{story['text'][:80]}...", use_column_width=True)
else:
    st.info("No stories added yet. Share yours above!")

# --- 👣 Footer ---
st.markdown("""
<div class='footer'>
Made with ❤️ by <b>Bhasha Builders</b> · Powered by Whisper, KeyBERT & Streamlit
</div>
""", unsafe_allow_html=True)
