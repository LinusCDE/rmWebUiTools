
import tkinter
from tkinter import *
from tkinter import ttk


class StatusWindow(tkinter.Tk):

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.files_done = 0
        self.total_files = 0

        self.title('Performing backup...')

        self.status_label = Label(self, text="0/0")
        self.status_label.grid(column=0, row=0)


        self.progress = ttk.Progressbar(self, orient="horizontal",
                                        length=200, mode="determinate")
        self.progress["maximum"] = 1
        self.progress["value"] = 0
        self.progress.grid(column=0, row=1)

    def set_total_files(self, total_files):
        self.total_files = total_files
        self.progress["maximum"] = total_files
        self.update_status_text()

    def update_status(self):
        self.files_done = self.files_done+1
        self.progress["value"] = self.files_done
        self.update_status_text()

    def update_status_text(self):
        self.status_label['text'] = str(self.files_done) + "/" + str(self.total_files)


