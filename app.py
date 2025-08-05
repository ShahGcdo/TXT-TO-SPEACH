import os
import tempfile
import gradio as gr
import torch
import torchaudio
import inflect
import re
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from moviepy.editor import AudioFileClip
import whisper

# Set font size for subtitles
rcParams.update({'font.size': 20})
p = inflect.engine()

# Load Whisper model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)

# Convert numbers to words, like 1947 → nineteen forty-seven
def convert_numbers_to_words(text):
    def replace(match):
        num = match.group()
        if len(num) == 4:
            return f"{p.number_to_words(num[:2])} {p.number_to_words(num[2:])}"
        return p.number_to_words(num)
    return re.sub(r'\b\d+\b', replace, text)

# Transcription function
def transcribe(audio):
    # Save temp file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_name = tmp.name
        audio.export(tmp_name, format="wav")

    result = model.transcribe(tmp_name)
    segments = result["segments"]
    
    # Plot waveform with white subtitle text (no yellow line)
    waveform, sample_rate = torchaudio.load(tmp_name)
    duration = waveform.shape[1] / sample_rate
    times = np.linspace(0, duration, waveform.shape[1])

    plt.figure(figsize=(10, 3))
    plt.plot(times, waveform[0].numpy(), color="white")
    plt.axis("off")

    # Add subtitle text (converted numbers)
    for segment in segments:
        start = segment['start']
        end = segment['end']
        mid = (start + end) / 2
        text = convert_numbers_to_words(segment['text'])
        plt.text(mid, 0, text, ha="center", va="center", fontsize=14, color="white", backgroundcolor="black")

    image_path = "subtitle_output.png"
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()

    os.remove(tmp_name)
    return image_path

# Gradio Interface
interface = gr.Interface(
    fn=transcribe,
    inputs=gr.Audio(source="upload", type="pydub"),
    outputs="image",
    title="Speech-to-Subtitle Converter",
    description="Upload audio and get a subtitle image with numbers spoken out like 'nineteen forty-seven'."
)

if __name__ == "__main__":
    interface.launch()
