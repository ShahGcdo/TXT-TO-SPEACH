import streamlit as st
from elevenlabs import generate, save, set_api_key
import whisper

# ----------- SETUP ----------
# 🔐 ElevenLabs API Key (Your key added here)
ELEVENLABS_API_KEY = "sk_6b2849ee7dbc95055d55ce2a11fb359848cfe5f049522226"
set_api_key(ELEVENLABS_API_KEY)

# Load Whisper model once
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

whisper_model = load_whisper_model()

# ----------- TTS FUNCTION ----------
def generate_audio(text, voice="Rachel", model="eleven_multilingual_v2"):
    audio = generate(text=text, voice=voice, model=model)
    save(audio, "output.mp3")
    return "output.mp3"

# ----------- WHISPER TIMING ----------
def get_timed_segments(audio_path):
    result = whisper_model.transcribe(audio_path)
    return result['segments']

# ----------- STREAMLIT UI ----------
st.title("🗣️ Multilingual Text-to-Speech with Pause Sync")
st.markdown("Generate realistic voiceovers in many languages, with pause timing via AI.")

text_input = st.text_area("🎤 Enter your text:", "Hello! Welcome to our multilingual AI voice demo.")
voice = st.selectbox("🗣️ Choose a voice:", ["Rachel", "Domi", "Bella", "Antoni", "Elli"])
generate_button = st.button("🔊 Generate Audio")

if generate_button:
    if not text_input.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Generating audio..."):
            audio_file = generate_audio(text_input, voice)
            st.success("✅ Audio generated!")

            # Playback
            st.audio(audio_file, format='audio/mp3')

        with st.spinner("Detecting pauses and transcribing..."):
            segments = get_timed_segments(audio_file)
            st.markdown("### 🧠 Pause-Synced Transcript:")
            for seg in segments:
                st.write(f"**{seg['start']:.2f}s – {seg['end']:.2f}s**: {seg['text']}")
