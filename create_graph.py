# create_graph.py
from pydub import AudioSegment
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import messagebox, Toplevel


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

def create_frequency_graph(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        samples = np.array(audio.get_array_of_samples())
        sample_rate = audio.frame_rate

        n = len(samples)
        freq = np.fft.rfftfreq(n, d=1 / sample_rate)
        fft = np.abs(np.fft.rfft(samples))

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.plot(freq, fft)
        ax.set_title('Frequency Spectrum')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Amplitude')
        ax.grid(True)
        plt.tight_layout()

        root_freq = Toplevel()
        root_freq.title("Frequency Graph")
        canvas = FigureCanvasTkAgg(fig, master=root_freq)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Frequency Graph Display Error", f"Error displaying frequency graph: {e}")
