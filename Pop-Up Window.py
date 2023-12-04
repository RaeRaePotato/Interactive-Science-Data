import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

gfile = ''
# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')

'''
tkinter.filedialog.askopenfilenames(**options)
Create an Open dialog and 
return the selected filename(s) that correspond to 
existing file(s).
'''
def select_file():
    filetypes = (
        ('Wav Filesg', '*.wav'),
        ('MP3 Audio Files', '*.mp3'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    gfile = filename

    # tkinter.messagebox — Tkinter message prompts
    showinfo(
        title='Selected File',
        message=filename
    )

    gfile_label = ttk.Label(root, text=gfile)
    gfile_label.pack(side="bottom")


# open button
open_button = ttk.Button(
    root,
    text='Load a file', #Load a file button
    command=select_file
)

open_button.pack(expand=True)


# run the application
root.mainloop()
