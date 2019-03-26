
import tkinter
from tkinter import ttk

class StatusWindow(tkinter.Tk):

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title('Performing backup...')
        self.geometry('300x100')
        self.progress = ttk.Progressbar(self, orient="horizontal",
                                        length=200, mode="determinate")
        self.progress["maximum"] = 100
        self.progress["value"] = 50
        self.progress.pack()


