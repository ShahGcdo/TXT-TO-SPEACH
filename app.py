import streamlit as st
import speech_recognition as sr
import time

def type_like_effect(text, speed=0.05):
    placeholder = st.empty()
    current_text = ""
    for char in text:
        current_text += char
        placeholder.markdown(current_text + "▌")
        time.sleep(speed)
    placeholder.markdown(current_text)

st.set_page_config(page_title="🎙 Voice to Typing", page_icon="🎤")
st.title("🎙 Voice Typing Effect (via Upload)")
st.markdown("Upload an audio file (.wav or .mp3) and see it typed out like you're speaking!")

audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3"])

if audio_file is not None:
    recognizer = sr.Recognizer()
    with sr.spinner("Transcribing..."):
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                result = recognizer.recognize_google(audio_data)
                st.success("✅ Transcription successful!")
                type_like_effect(result, speed=0.05)
            except sr.UnknownValueError:
                st.error("❌ Could not understand audio.")
            except sr.RequestError as e:
                st.error(f"API error: {e}")
