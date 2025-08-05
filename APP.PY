import streamlit as st
import speech_recognition as sr
import time

# Typing animation function
def type_like_effect(text, speed=0.05):
    placeholder = st.empty()
    current_text = ""
    for char in text:
        current_text += char
        placeholder.markdown(current_text + "▌")
        time.sleep(speed)
    placeholder.markdown(current_text)

# Streamlit page setup
st.set_page_config(page_title="Live Voice Typing", page_icon="🎙")
st.title("🎙 Live Voice Typing")
st.markdown("Speak and watch your words appear like you're typing in real time!")

# Button to trigger recording
if st.button("🎤 Start Speaking"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak clearly.")
        audio = recognizer.listen(source)

    try:
        with st.spinner("Transcribing your speech..."):
            result = recognizer.recognize_google(audio)
            st.success("✅ Transcription successful!")
            type_like_effect(result, speed=0.05)

    except sr.UnknownValueError:
        st.error("😕 Sorry, couldn't understand what you said.")
    except sr.RequestError as e:
        st.error(f"⚠️ Could not request results; {e}")
