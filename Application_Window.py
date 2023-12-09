import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pydub import AudioSegment
from mutagen import File
import os


class Model:
    def __init__(self):
        self.input_file = ''
        self.converted_file = ''
        self.root = tk.Tk()
        self.root.title('Tkinter Open File Dialog')
        self.root.resizable(False, False)
        self.root.geometry('500x250')

        # Create self.audio_length_label as a class attribute
        self.audio_length_label = ttk.Label(self.root, text='Audio Length: N/A')
        self.audio_length_label.pack(side="bottom")

    def convert_to_wav(self, input_file):
        try:
            _, input_extension = os.path.splitext(input_file)
            if input_extension.lower() == '.wav':
                self.input_file = input_file
                return input_file, 'wav'  # Return the original .wav file and format
            else:
                audioclip = AudioSegment.from_file(input_file, format=input_extension[1:])
                output_file = "UpdatedClap.wav"
                audioclip.export(output_file, format="wav")
                self.input_file = output_file
                return output_file, input_extension[1:]  # Return the new .wav file and format
        except Exception as e:
            messagebox.showerror("Conversion Error", f"Error converting file: {e}")
            return None, None

    def remove_metadata_tags(self, input_file):
        try:
            audio = File(input_file)
            audio.delete()
            audio.save()
        except Exception as e:
            messagebox.showerror("Metadata Removal Error", f"Error removing metadata: {e}")

    def is_multi_chan(self, input_file):
        try:
            audioclip = AudioSegment.from_file(input_file)
            return audioclip.channels == 2
        except Exception as e:
            messagebox.showerror("Channel Check Error", f"Error checking channels: {e}")
            return False

    def audio_length(self):
        try:
            if self.input_file:
                if self.input_file.lower().endswith('.wav'):
                    audioclip = AudioSegment.from_file(self.input_file)
                else:
                    original_file = os.path.splitext(self.input_file)[0] + os.path.splitext(self.converted_file)[1]
                    audioclip = AudioSegment.from_file(original_file)

                duration_seconds = audioclip.duration_seconds
                self.audio_length_label.config(text=f'Audio Length: {duration_seconds:.2f} seconds')
        except Exception as e:
            messagebox.showerror("Duration Calculation Error", f"Error calculating duration: {e}")

    def run(self):
        try:
            open_button = ttk.Button(self.root, text='Load a file', command=self.select_file)
            open_button.pack(expand=True)

            # Run the application window
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")

    def select_file(self):
        try:
            filetypes = (
                ('Audio Files', ('*.wav', '.mp3')),
                ('All files', '*.*')
            )

            filename = filedialog.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)

            if filename:
                _, file_extension = os.path.splitext(filename)
                new_file, new_format = self.convert_to_wav(filename)
                if new_file is not None:
                    self.converted_file = new_file
                    messagebox.showinfo('File Converted', f'Selected file converted to .wav: {self.converted_file}')
                    self.remove_metadata_tags(self.converted_file)
                    gfile_label = ttk.Label(self.root, text=f'{self.converted_file} (Format: {new_format})')
                    gfile_label.pack(side="bottom")
                    if file_extension.lower() != '.wav':
                        self.input_file = self.converted_file
                    self.audio_length()

                    # Schedule the show_waveform method after 500 milliseconds
                    self.root.after(500, self.show_waveform)
        except Exception as e:
            messagebox.showerror("File Selection Error", f"Error selecting file: {e}")

    def run(self):
        try:
            open_button = ttk.Button(self.root, text='Load a file', command=self.select_file)
            open_button.pack(expand=True)

            # Schedule the show_waveform method after 500 milliseconds
            self.root.after(500, self.show_waveform)

            # Run the application window
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")

    def show_waveform(self):
        try:
            if self.converted_file and os.path.exists(self.converted_file):
                import create_graph
                create_graph.display_waveform(self.converted_file)
            else:
                messagebox.showinfo("No File Selected", "Please load an audio file before displaying the waveform.")
        except Exception as e:
            messagebox.showerror("Waveform Display Error", f"Error displaying waveform: {e}")


# Create an instance of the Model class and run the application
model_instance = Model()
model_instance.run()
