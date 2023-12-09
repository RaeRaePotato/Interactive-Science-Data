import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from pydub import AudioSegment
import os
from mutagen import File
from create_graph import display_waveform

class Model:
    def __init__(self):
        self.input_file = ''
        self.gfile = ''
        self.root = tk.Tk()
        self.root.title('Tkinter Open File Dialog')
        self.root.resizable(False, False)
        self.root.geometry('500x250')

    def convert_to_wav(self, input_file):
        _, input_extension = os.path.splitext(input_file)
        if input_extension.lower() == '.wav':
            return input_file, 'wav'  # Return the original .wav file and format

        else:
            audioclip = AudioSegment.from_file(input_file, format=input_extension[1:])
            self.input_file = audioclip.export("UpdatedClap.wav", format="wav")
            return "UpdatedClap.wav", input_extension[1:]  # Return the new .wav file and format

    def remove_metadata_tags(self, input_file):
        audio = File(input_file)
        audio.delete()
        audio.save()

    def select_file(self):
        filetypes = (
            ('Audio Files', ('*.wav', '.mp3')),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        if filename:
            _, file_extension = os.path.splitext(filename)
            if file_extension.lower() == '.wav':
                self.gfile, new_format = filename, 'wav'
                showinfo(
                    title='Selected File',
                    message=f'Selected .wav file: {filename}'
                )
            else:
                new_file, new_format = self.convert_to_wav(filename)
                self.gfile = new_file
                showinfo(
                    title='File Converted',
                    message=f'Selected file converted to .wav: {self.gfile}'
                )

                # Remove metadata tags from the newly created file
                self.remove_metadata_tags(self.gfile)

            # Update gfile_label only once, outside of the if-else block
            gfile_label = ttk.Label(self.root, text=f'{self.gfile} (Format: {new_format})')
            gfile_label.pack(side="bottom")


            self.remove_metadata_tags(self.gfile)

            # Display waveform of the selected file
            display_waveform(self.gfile)

    def single_channel(self):
        if self.is_multi_chan(self.input_file):
            audioclip = AudioSegment.from_wav(self.input_file).set_channels(1)
            # Assuming you want to convert to wav and update input_file
            self.input_file, new_format = self.convert_to_wav(audioclip)
            showinfo(
                title='Single Channel',
                message=f'Single channel applied. Updated file: {self.input_file} (Format: {new_format})'
            )
        else:
            showinfo(
                title='Single Channel',
                message='The input file does not have 2 channels. No action taken.'
            )

    def is_multi_chan(self, input_file):
        audioclip = AudioSegment.from_file(input_file)
        return audioclip.channels == 2

    def run(self):
        # open button
        open_button = ttk.Button(self.root, text='Load a file', command=self.select_file)
        open_button.pack(expand=True)

        # run the application
        self.root.mainloop()

# Create an instance of the Model class and run the application
model_instance = Model()
model_instance.run()
