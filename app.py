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

st.set_page_config(page_title="BhashaBeat", layout="centered", page_icon="🎙️")

# Load custom CSS stylesheet
css_path = "assets/style.css"
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header Section
st.markdown('<div class="gradient-text">🎙️ BhashaBeat</div>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 1.15rem; color: #9ca3af; margin-bottom: 2rem;">Voice of the People – Preserving oral heritage through AI.</p>', unsafe_allow_html=True)

# Calculate live metrics
total_stories = len(df)
if total_stories > 0:
    unique_langs = df["language"].nunique()
    # Extract unique keywords
    all_kws = []
    for kws in df["keywords"].dropna():
        if isinstance(kws, str) and kws.strip():
            all_kws.extend([k.strip() for k in kws.split(",")])
    total_kws = len(set(all_kws))
else:
    unique_langs = 0
    total_kws = 0

# Metrics Dashboard
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="stat-card"><div class="stat-val">{total_stories}</div><div class="stat-lbl">Contributions</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-card"><div class="stat-val">{unique_langs}</div><div class="stat-lbl">Languages</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="stat-card"><div class="stat-val">{total_kws}</div><div class="stat-lbl">Keywords</div></div>', unsafe_allow_html=True)
st.markdown('<div style="margin-bottom: 2.5rem;"></div>', unsafe_allow_html=True)

# Form Section
tab1, tab2 = st.tabs(["🗣️ Record Voice", "⌨️ Enter Text"])

with tab1:
    st.markdown("### Upload Audio Recording")
    uploaded_audio = st.file_uploader("Upload your voice (.wav/.mp3)", type=["wav", "mp3"])
    if uploaded_audio:
        st.audio(uploaded_audio)
        if st.button("Transcribe & Save Story"):
            with st.spinner("Transcribing speech..."):
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

                st.success("Story successfully preserved!")
                if summary != text:
                    st.markdown(f'<div class="story-summary"><strong>Generated Summary:</strong> {summary}</div>', unsafe_allow_html=True)
                st.image(image_path, caption="Generated Story Tile")
                os.remove(temp_path)
                st.rerun()

with tab2:
    st.markdown("### Write Story Details")
    text_input = st.text_area("Type your story, idiom, or proverb here", height=150)
    if st.button("Save Written Story"):
        if text_input.strip() == "":
            st.warning("Please enter some text before saving.")
        else:
            with st.spinner("Analyzing text..."):
                lang = detect_language(text_input)
                keywords = extract_keywords(text_input)
                summary = summarize_text(text_input)
                image_path = create_story_tile(text_input, keywords)

                timestamp = datetime.datetime.now().isoformat()
                df.loc[len(df)] = [timestamp, text_input, lang, ",".join(keywords), summary, image_path]
                df.to_csv(DATA_FILE, index=False)

                st.success("Story successfully preserved!")
                if summary != text_input:
                    st.markdown(f'<div class="story-summary"><strong>Generated Summary:</strong> {summary}</div>', unsafe_allow_html=True)
                st.image(image_path, caption="Generated Story Tile")
                st.rerun()

# Stories Feed Section
st.markdown('<div style="margin-top: 3.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<h2 style="margin-bottom: 1.5rem;">📖 Preserved Oral Stories</h2>', unsafe_allow_html=True)

if len(df):
    df_sorted = df.copy()
    if "timestamp" in df_sorted.columns:
        try:
            df_sorted["datetime"] = pd.to_datetime(df_sorted["timestamp"])
            df_sorted = df_sorted.sort_values(by="datetime", ascending=False)
        except:
            pass
            
    for idx, row in df_sorted.iterrows():
        lang_name = str(row["language"]).upper()
        if lang_name == "TE":
            lang_name = "Telugu"
        elif lang_name == "EN":
            lang_name = "English"
        elif lang_name == "HI":
            lang_name = "Hindi"
            
        raw_date = row["timestamp"]
        try:
            formatted_date = pd.to_datetime(raw_date).strftime("%b %d, %Y - %I:%M %p")
        except:
            formatted_date = str(raw_date)[:16]
            
        kw_list = []
        if isinstance(row["keywords"], str) and row["keywords"].strip():
            kw_list = [k.strip() for k in row["keywords"].split(",")]
        kw_badges_html = "".join([f'<span class="kw-badge">#{k}</span>' for k in kw_list])
        
        story_text = row["text"]
        summary_text = row.get("summary", "")
        
        summary_html = ""
        if isinstance(summary_text, str) and summary_text.strip() and summary_text != story_text:
            summary_html = f'<div class="story-summary"><strong>AI Summary:</strong> {summary_text}</div>'
            
        img_path = row["image_path"]
        
        card_html = f"""
        <div class="glass-card">
            <div class="story-header">
                <span class="lang-badge">{lang_name}</span>
                <span class="story-date">⏱️ {formatted_date}</span>
            </div>
            <div class="story-text">"{story_text}"</div>
            {summary_html}
            <div class="badge-container">
                {kw_badges_html}
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Tile Download Button
        if isinstance(img_path, str) and os.path.exists(img_path):
            col_btn, _ = st.columns([1, 3])
            with col_btn:
                with open(img_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Story Tile",
                        data=file,
                        file_name=os.path.basename(img_path),
                        mime="image/jpeg",
                        key=f"dl_{idx}"
                    )
            st.markdown('<div style="margin-bottom: 20px;"></div>', unsafe_allow_html=True)
else:
    st.info("No oral heritage stories preserved yet. Be the first to share one!")

# Developer View
st.markdown("---")
with st.expander("🛠️ Advanced Researcher Database View"):
    st.dataframe(df)
