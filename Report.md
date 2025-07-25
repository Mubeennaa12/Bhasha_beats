Project Report: BhashaBeat
1.1 Team Information
Team Name: Bhasha Builders
Team Members: Pervez Mubeen, Yashaswi Darga, Snigdha Somaraju, Pranathi Bandi, Srivarsha Chivukula

1.2 Application Overview
BhashaBeat is a multilingual, offline-first application that allows users to record or type short stories in their local language. These stories are transcribed, tagged, and visualized as shareable “story tiles.” The MVP collects culturally rich Telugu stories and proverbs via voice/text input and stores them as both images and text data.

1.3 AI Integration Details
Speech-to-text: openai/whisper-small

Language Detection: langdetect

Keyword Extraction: keyBERT

Tile Generator: PIL

All models are open-source and used locally.

1.4 Technical Architecture & Development
Frontend: Streamlit

Backend: Python

Models: Transformers (Whisper), keybert, langdetect

Image Generation: Pillow

Data Storage: CSV

Deployment: Hugging Face Spaces

1.5 User Testing & Feedback
Methodology: 10 Telugu-speaking users tested via file uploads.

Feedback collected on: accuracy, ease of use, shareability.

Iterations included: font fallback, improved keyword clarity, better UI messages.

1.6 Project Lifecycle & Roadmap
A. Week 1 – Development Sprint
Built core MVP: voice/text input, whisper transcription, keyword extractor, tile creation, CSV storage.

B. Week 2 – Beta Testing & Iteration
Users: Local students and storytellers
Feedback: Faster processing, clearer images, easier sharing
Implemented: Tile styling, default font fallback, download button

C. Weeks 3–4 – User Acquisition & Corpus Growth

Target Audience: Telugu users, folk artists, students

Channels: WhatsApp groups, Telugu literature pages

Strategy: Promote cultural preservation + social media sharing

Metrics:

Users: 320+ in 2 weeks

Corpus Entries: 850+ stories

Languages: 90% Telugu, 10% mixed (Hindi, English)

D. Post-Internship Vision

Add community voting/upvoting

Multilingual UI support (e.g., Hindi, Tamil, Kannada)

Integrate vector embeddings + search

Collect image/audio-text pairs for AI training

—

📦 3. requirements.txt

streamlit
transformers
torch
torchaudio
langdetect
keybert
Pillow
scikit-learn
sentence-transformers
accelerate
numpy

—