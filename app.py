import streamlit as st
from moviepy.editor import TextClip, CompositeVideoClip
import tempfile
import os

st.set_page_config(page_title="📝 Text to Scrolling Video", page_icon="🎥")
st.title("📝 Text to Scrolling Video Generator")
st.markdown("Paste your text, generate a scrolling video, preview it, and download! 🎬")

text_input = st.text_area("✍️ Paste your text here", height=200)
generate_button = st.button("🎬 Generate Video")

if generate_button and text_input.strip() != "":
    with st.spinner("Generating video..."):

        # Generate a scrolling text clip
        txt_clip = TextClip(text_input, fontsize=40, color='white', size=(720, 1280), method='caption', font="Arial")
        scroll_clip = txt_clip.set_duration(10).set_position(("center", "center")).on_color(color=(0, 0, 0), col_opacity=1)

        # Save to temporary file
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, "scrolling_text.mp4")
        scroll_clip.write_videofile(video_path, fps=24, codec='libx264')

        st.success("✅ Video generated!")

        # Preview and Download
        st.video(video_path)
        with open(video_path, "rb") as f:
            st.download_button("⬇️ Download Video", f, file_name="scrolling_text.mp4", mime="video/mp4")
