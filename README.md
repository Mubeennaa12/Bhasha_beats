# bhashabeats



BhashaBeat
BhashaBeat is a multilingual, offline-first Streamlit application that invites users to contribute personal stories, idioms, or proverbs in their mother tongue—via text or voice. The app transcribes voice input using Whisper, extracts keywords, and creates beautiful story tiles for easy sharing. Designed for low-bandwidth users, it helps preserve India’s oral heritage while collecting high-quality linguistic data.

Features
🎙️ Voice & Text Input (Telugu & more)

🧠 Speech-to-text using Whisper

🗣️ Language Detection with langdetect

🔑 Keyword Extraction via KeyBERT

🖼️ Image Tile Generator with PIL

📦 Offline-first and shareable design

📥 Data saved to local CSV (stories.csv)

Try It Now
Run locally:

bash
Copy
Edit
git clone https://your-repo-url
cd bhasha_beat
pip install -r requirements.txt
streamlit run app.py
MVP Stack
Streamlit

openai/whisper-small (via transformers)

langdetect

keybert

Pillow

Python 3.9+

—