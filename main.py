import tkinter as tk
import toolbar as tb
import playground as pg
# import Bottomtools as bt
from PIL import ImageTk, Image

window = tk.Tk()
window.configure(background="#1f1f1f")
window.resizable(False, False)
window.title("Image Cropping")
frm_tb = tk.Frame(window)
frm_pg = tk.Frame(window)
frm_tb.configure(background="#1f1f1f")
frm_pg.configure(background="#1f1f1f", padx=150, pady=150)

frm_tb.pack(side='left')
frm_pg.pack(side='left')

playground = pg.Playground(frm_pg)
toolbar = tb.Toolbar(frm_tb, playground)

#### Event handler for key press: "Enter"
window.bind("<Return>", playground.keyPressed)

tk.mainloop()