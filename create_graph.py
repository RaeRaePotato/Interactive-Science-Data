# create_graph.py
from pydub import AudioSegment
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.io import wavfile
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


class Frequency:
    sample_rate, data = wavfile.read("UpdatedClap.wav")

    def find_target_frequency(self, freqs):
        for x in freqs:
            if x > 1000:
                break
        return x

    def frequency_check(self):  # identify a frequency to check
        # print(freqs)
        global target_frequency
        target_frequency = self.find_target_frequency(self.freqs)
        index_of_frequency = np.where(self.freqs == target_frequency)[0][0]
        # find sound data for a particular frequency data_for_frequency = spectrum[index_of_frequency]
        # change a digital signal
        data_in_db_fun = 10 * np.log10(data_for_frequency)
        return data_in_db_fun

    def find_nearest_value(array, value):
        array = np.asarray(array)

        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def plot_rt60(self):
        data_in_db = self.frequency_check()
        plt.figure(2)

        plt.plot(self.t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')

        # Get the index of the max value
        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        plt.plot(self.t[index_of_max], data_in_db[index_of_max], 'go')

        # Cut the array from the max value
        sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5

        # Find the closest value < 5db
        value_of_max_less_5 = self.find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)

        plt.plot(self.t[index_of_max_less_5], data_in_db[index_of_max_less_5], 'yo')

        # Cut the array from -5db
        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = self.find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
        plt.plot(self.t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

        rt20 = (self.t[index_of_max_less_5] - self.t[self.index_of_max_les_25])[0]
        # print (f'rt20= {rt20}')
        rt60 = 3 * rt20
        # plt.xlim(0, ((round(abs(rt60), 2)) * 1.5))
        plt.grid()
        plt.show()
        print(f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)} seconds')

    # RT60 Difference
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











