"""
CTkPDFViewer is a pdf viewer widget for customtkinter.
Author: Akash Bora
License: MIT
Version 2 Work By MaxNiark
"""

import customtkinter
from tkinter import ttk
from PIL import Image, ImageTk
import fitz as fz
from threading import Thread
import math
import io
import os

class CTkPDFViewer(customtkinter.CTkFrame):

    def __init__(self,
                 master: any,
                 file: str,
                 width: int = 600,
                 height: int = 200,
                 page_width: int = 600,
                 page_height: int = 700,
                 page_separation_height: int = 2,
                 **kwargs):
        
        super().__init__(master, width=width, height=height,**kwargs)

        def on_window_resize(event):
            width = event.width
            height = event.height
            print(f"Window resized to {width}x{height}")

        # Bind the resize event to a function
        self.master.bind("<Configure>", on_window_resize)
        self._scrlframe = customtkinter.CTkScrollableFrame(self, width=page_width)
        self._scrlframe.grid(row=0, column=0, sticky="nesw")

        self.page_width = page_width
        self.page_height = page_height
        self.separation = page_separation_height
        self.pdf_images = []
        self.labels = []
        self._pdf = ""

        self.file = file
        self.percentage_view = 0
        self.percentage_load = customtkinter.StringVar()
        
        self.loading_message = customtkinter.CTkLabel(self, textvariable=self.percentage_load, justify="center")
        self.loading_bar = customtkinter.CTkProgressBar(self, width=100)
        self.loading_bar.set(0)
        
        self.grid_columnconfigure(0, weight=1, minsize=200)
        self.grid_rowconfigure(0, weight=1, minsize=10)
        self._grid_loading()

    def start_process(self):
        self._ADD_PAGE()

    def _grid_loading(self):
        self.loading_message.grid(row=0, column=0)
        self.loading_bar.grid(row=0)
        self.after(250, self.start_process)

    def _ADD_PAGE(self):
        self.percentage_bar = 0
        pdf = fz.open(self.file)
        count = 0
        for page in pdf:
            page_data = page.get_pixmap()
            pix = fz.Pixmap(page_data, 0) if page_data.alpha else page_data
            img = Image.open(io.BytesIO(pix.tobytes('ppm')))
            label_img = ImageTk.PhotoImage(img, size=(self.page_width+150, self.page_height), width=750)
            self.pdf_images.append(label_img)
            
            self.percentage_bar += 1
            percentage_view = (float(self.percentage_bar) / float(len(pdf)) * float(100))
            self.loading_bar.set(percentage_view)
            self.percentage_load.set(f"Loading {os.path.basename(self.file)} \n{int(math.floor(percentage_view))}%")
        
        self.loading_bar.grid_forget()
        self.loading_message.grid_forget()

        pdf.close()
        
        for i in self.pdf_images:
            label = ttk.Label(self._scrlframe, image=i, text="")
            label.grid(row=count, column=0, pady=(0 + self.separation), sticky="nesw")
            count += 1
            self.labels.append(label)

    def configure(self, **kwargs):
        """ configurable options """
        if "file" in kwargs:
            self.file = kwargs.pop("file")
            self.pdf_images = []

            for i in self.labels:
                i.destroy()

            self.labels = []
            self.after(250, self._grid_loading)
            
        if "page_width" in kwargs:
            self.page_width = kwargs.pop("page_width")
            for i in self.pdf_images:
                i.configure(size=(self.page_width, self.page_height))
                
        if "page_height" in kwargs:
            self.page_height = kwargs.pop("page_height")
            for i in self.pdf_images:
                i.configure(size=(self.page_width, self.page_height))
            
        if "page_separation_height" in kwargs:
            self.separation = kwargs.pop("page_separation_height")
            for i in self.labels:
                i.pack_forget()
                i.pack(pady=(0, self.separation))
        
        super().configure(**kwargs)
