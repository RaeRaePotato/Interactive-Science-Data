# create_graph.py
import matplotlib.pyplot as plt
from pydub import AudioSegment
import numpy as np

def display_waveform(file_path):
    audio = AudioSegment.from_file(file_path)
    samples = np.array(audio.get_array_of_samples())
    sample_rate = audio.frame_rate

    time = np.arange(0, len(samples)) / sample_rate  # Calculate time array

    plt.figure(figsize=(6.5, 5.5))
    plt.plot(time, samples)
    plt.title('Audio Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.tight_layout()

    plt.show()
