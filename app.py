import streamlit as st
import os
import pandas as pd
from utils import transcribe_audio, detect_language, extract_keywords, create_story_tile, summarize_text
import datetime

# CSV path
DATA_FILE = "data/stories.csv"
os.makedirs("data", exist_ok=True)

# Load CSV or initialize
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    if "summary" not in df.columns:
        df["summary"] = ""
else:
    df = pd.DataFrame(columns=["timestamp", "text", "language", "keywords", "summary", "image_path"])

st.set_page_config(page_title="BhashaBeat", layout="centered")
st.title("🎙️ BhashaBeat – Voice of the People")
st.markdown("Share your stories, idioms, or proverbs in your native tongue.")

tab1, tab2 = st.tabs(["🗣️ Record Voice", "⌨️ Enter Text"])

with tab1:
    uploaded_audio = st.file_uploader("Upload your voice (.wav/.mp3)", type=["wav", "mp3"])
    if uploaded_audio:
        st.audio(uploaded_audio)
        if st.button("Transcribe & Save"):
            with st.spinner("Transcribing..."):
                temp_path = f"temp_{uploaded_audio.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_audio.read())

                text = transcribe_audio(temp_path)
                lang = detect_language(text)
                keywords = extract_keywords(text)
                summary = summarize_text(text)
                image_path = create_story_tile(text, keywords)

                timestamp = datetime.datetime.now().isoformat()
                df.loc[len(df)] = [timestamp, text, lang, ",".join(keywords), summary, image_path]
                df.to_csv(DATA_FILE, index=False)

                st.success("Story added!")
                if summary != text:
                    st.write(f"**Summary:** {summary}")
                st.image(image_path, caption="Your Story Tile")
                os.remove(temp_path)

with tab2:
    text_input = st.text_area("Type your story, idiom, or proverb here")
    if st.button("Save Text Story"):
        if text_input.strip() == "":
            st.warning("Please enter some text.")
        else:
            lang = detect_language(text_input)
            keywords = extract_keywords(text_input)
            summary = summarize_text(text_input)
            image_path = create_story_tile(text_input, keywords)

            timestamp = datetime.datetime.now().isoformat()
            df.loc[len(df)] = [timestamp, text_input, lang, ",".join(keywords), summary, image_path]
            df.to_csv(DATA_FILE, index=False)

            st.success("Story added!")
            if summary != text_input:
                st.write(f"**Summary:** {summary}")
            st.image(image_path, caption="Your Story Tile")

st.markdown("---")
st.subheader("📖 Your Stories So Far")
if len(df):
    st.dataframe(df[["timestamp", "text", "language", "keywords", "summary"]])
else:
    st.info("No stories added yet.")
