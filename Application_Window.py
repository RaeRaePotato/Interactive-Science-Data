import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from pydub import AudioSegment
import os


class Model:
    def __init__(self):
        self.input_file = ''

    gfile = ''
    root = tk.Tk()
    root.title('Tkinter Open File Dialog')
    root.resizable(False, False)
    root.geometry('500x250')


def convert_to_wav(input_file):
    _, input_extension = os.path.splitext(input_file)
    if input_extension.lower() == '.wav':
        return input_file, 'wav'  # Return the original .wav file and format

    else:
        audioclip = AudioSegment.from_file(input_file, format=input_extension[1:])
        Model.input_file = audioclip.export("UpdatedClap.wav", format="wav")
        return "UpdatedClap.wav", input_extension[1:]  # Return the new .wav file and format


def select_file():
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
            Model.gfile, new_format = filename, 'wav'
            showinfo(
                title='Selected File',
                message=f'Selected .wav file: {filename}'
            )
        else:
            new_file, new_format = convert_to_wav(filename)
            Model.gfile = new_file
            showinfo(
                title='File Converted',
                message=f'Selected file converted to .wav: {Model.gfile}'
            )

        # Update gfile_label only once, outside of the if-else block
        gfile_label = ttk.Label(Model.root, text=f'{Model.gfile} (Format: {new_format})')
        gfile_label.pack(side="bottom")


# open button
open_button = ttk.Button(Model.root, text='Load a file', command=select_file)
open_button.pack(expand=True)

# run the application
Model.root.mainloop()
