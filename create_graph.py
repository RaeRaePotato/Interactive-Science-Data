# create_graph.py
from pydub import AudioSegment
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
from tkinter import messagebox, Toplevel
import wave as wav



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


class Frequency:
    sample_rate, data = wavfile.read("UpdatedClap.wav")

    def find_target_frequency(self, freqs, target_freq):
        # Find the nearest frequency in the spectrum to the target frequency
        return min(freqs, key=lambda x: abs(x - target_freq))

    def frequency_check(self, target_freq):  # identify a frequency to check
        index_of_frequency = np.where(self.freqs == target_freq)[0][0]
        data_for_frequency = self.spectrum[index_of_frequency]
        # change a digital signal
        data_in_db_fun = 10 * np.log10(self.data_for_frequency)
        return data_in_db_fun

    def create_frequency_graph(self, target_freq, title):
        try:
            data_in_db = self.frequency_check(target_freq)

            fig, ax = plt.subplots(figsize=(7, 5))
            ax.plot(self.t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
            ax.set_title(title)
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Power (dB)')

            # Get the index of the max value
            index_of_max = np.argmax(data_in_db)
            ax.plot(self.t[index_of_max], data_in_db[index_of_max], 'go')

            # Cut the array from the max value
            sliced_array = data_in_db[index_of_max:]
            value_of_max_less_5 = data_in_db[index_of_max] - 5

            # Find the closest value < 5db
            value_of_max_less_5 = self.find_nearest_value(sliced_array, value_of_max_less_5)
            index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
            ax.plot(self.t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')
#Cut the array from -5db
            value_of_max_less_25 = data_in_db[index_of_max] - 25
            value_of_max_less_25 = self.find_nearest_value(sliced_array, value_of_max_less_25)
            index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
            ax.plot(self.t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

            plt.grid()
            plt.tight_layout()

            return fig

        except Exception as e:
            messagebox.showerror("Frequency Graph Display Error", f"Error displaying frequency graph: {e}")

    def create_high_mid_low_frequency_graphs(self):
        high_freq = 2000  # Set the high-frequency threshold
        mid_freq = 1000   # Set the mid-frequency threshold

        high_freq_graph = self.create_frequency_graph(high_freq, 'High Frequency Spectrum')
        mid_freq_graph = self.create_frequency_graph(mid_freq, 'Mid Frequency Spectrum')

        low_freq_graph = plt.figure(figsize=(7, 5))
        low_freq_ax = low_freq_graph.add_subplot(111)
        low_freq_ax.plot(self.t, self.data, color='green')
        low_freq_ax.set_title('Low Frequency Spectrum')
        low_freq_ax.set_xlabel('Time (s)')
        low_freq_ax.set_ylabel('Amplitude')
        low_freq_ax.grid(True)
        plt.tight_layout()

        return high_freq_graph, mid_freq_graph, low_freq_graph

    def rt60_difference(self):
        data_in_db = self.frequency_check()
        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5
        value_of_max_less_5 = self.find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)

        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = self.find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
        rt20 = (self.t[index_of_max_less_5] - self.t[index_of_max_less_25])[0]

        rt60 = rt20 * 3
        print('%.3f' % abs(rt60))
        return '%.3f' % (abs(rt60) - 0.5)

    def high_freq(self):

        with wav.open(self.input_file, 'r') as audio_file:
            signal = np.frombuffer(audio_file.readframes(-1), dtype=np.int16)
        high_slice = int(len(signal) * 0.4)
        high_wave = signal[:high_slice]
        plt.figure(figsize=(8, 4))
        plt.plot(high_wave, 'g')
        plt.ylabel('Amplitude')
        plt.xlabel('Time')
        plt.title('High Wave-form')
        plt.show()

        self.set_file_path('UpdatedClap.wav')
        return high_wave

    def mid_freq(self):
        # opens the wav file for reading to pull signal, then closes it
        with wav.open(self.input_file, 'r') as audio_file:
            signal = np.frombuffer(audio_file.readframes(-1), dtype=np.int16)

        # cuts signify areas of the signal that represent different frequencies or power
        high_slice = int(len(signal) * 0.4)
        mid_slice = int(len(signal) * 0.6)
        mid_wave = signal[high_slice:mid_slice]

        # plot the signal
        plt.figure(figsize=(8, 4))
        plt.plot(mid_wave, 'y')
        plt.ylabel('Amplitude')
        plt.xlabel('Time')
        plt.title('Mid Wave-form')
        plt.show()

        # reinitialize the file, as wave closes the file once the function is complete
        self.set_file_path('UpdatedClap.wav')

        # passing the modified signal for possible future use
        return mid_wave

    def low_freq(self):
        # opens the wav file for reading to pull signal, then closes it
        with wav.open(self.input_file, 'r') as audio_file:
            signal = np.frombuffer(audio_file.readframes(-1), dtype=np.int16)

        # cuts signify areas of the signal that represent different frequencies or power
        mid_slice = int(len(signal) * 0.6)
        low_wave = signal[mid_slice:]

        # plotting the waveform
        plt.figure(figsize=(8, 4))
        plt.plot(low_wave, 'r')
        plt.ylabel('Amplitude')
        plt.xlabel('Time')
        plt.title('Low Wave-form')
        plt.show()

        # reinitialize the file, as wave closes the file once the function is complete
        self.set_file_path('UpdatedClap.wav')

        # passing the modified signal for possible future use
        return low_wave













