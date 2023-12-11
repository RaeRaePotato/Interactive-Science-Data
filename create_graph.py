# create_graph.py
from pydub import AudioSegment
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import messagebox
import tkinter as tk


def create_waveform(root, file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        samples = np.array(audio.get_array_of_samples())
        sample_rate = audio.frame_rate
        time = np.arange(0, len(samples)) / sample_rate

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.plot(time, samples)
        ax.set_title('Audio Waveform')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        ax.grid(True)
        plt.tight_layout()

        waveform_canvas = FigureCanvasTkAgg(fig, master=root)
        waveform_canvas.draw()
        waveform_canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Waveform Display Error", f"Error displaying waveform: {e}")


