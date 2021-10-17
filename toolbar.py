import tkinter as tk
from PIL import ImageTk, Image

NRM = "normal"
VRT = "vertical"
HOR = "horizontal"


class Toolbar:
    
    #### This is a big mistake :( Surely i could have done this in loops and in generic way
    
    def __init__(self, master, playground) -> None:
        self.playground = playground
        self.master = master

        self.btn_nrm_crp = tk.Button(self.master, text="Normal cropping", command=self.select_nrm)
        self.btn_nrm_crp.configure(font=("Arial", 15), width=17, bg="#1f1f1f", fg="#f0f0f0", relief=tk.FLAT, borderwidth=0, pady=5)
        self.btn_nrm_crp.pack(padx=6, pady=6)
        self.btn_vrt_crp = tk.Button(self.master, text="Vertical cropping", command=self.select_vrt)
        self.btn_vrt_crp.configure(font=("Arial", 15), width=17, bg="#1f1f1f", fg="#f0f0f0", relief=tk.FLAT, borderwidth=0)
        self.btn_vrt_crp.pack(padx=6, pady=6)
        self.btn_hor_crp = tk.Button(self.master, text="Horizontal cropping", command=self.select_hor)
        self.btn_hor_crp.configure(font=("Arial", 15), width=17, bg="#1f1f1f", fg="#f0f0f0", relief=tk.FLAT, borderwidth=0)
        self.btn_hor_crp.pack(padx=6, pady=6)
        
        playground.mode = NRM
        self.selected_tool = NRM
        self.btn_nrm_crp.configure(relief=tk.SUNKEN, bg="#1a1a1a", borderwidth=1)
        # remove sunken attribute from selected widget

    def select_nrm(self):
        self.playground.mode = NRM
        self.playground.reset()
        self.selected_tool = NRM
        self.btn_nrm_crp.configure(relief=tk.SUNKEN, bg="#1a1a1a", borderwidth=1)
        self.btn_vrt_crp.configure(relief=tk.FLAT, bg="#1f1f1f", borderwidth=0)
        self.btn_hor_crp.configure(relief=tk.FLAT, bg="#1f1f1f", borderwidth=0)
    
    def select_vrt(self):
        self.playground.mode = VRT
        self.playground.reset()
        self.selected_tool = VRT
        self.btn_nrm_crp.configure(relief=tk.FLAT, bg="#1f1f1f", borderwidth=0)
        self.btn_vrt_crp.configure(relief=tk.SUNKEN, bg="#1a1a1a", borderwidth=1)
        self.btn_hor_crp.configure(relief=tk.FLAT, bg="#1f1f1f", borderwidth=0)
    
    def select_hor(self):
        self.playground.mode = HOR
        self.playground.reset()
        self.selected_tool = HOR
        self.btn_nrm_crp.configure(relief=tk.FLAT, bg="#1f1f1f", borderwidth=0)
        self.btn_vrt_crp.configure(relief=tk.FLAT, bg="#1f1f1f", borderwidth=0)
        self.btn_hor_crp.configure(relief=tk.SUNKEN, bg="#1a1a1a", borderwidth=1)
    