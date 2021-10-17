import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from PIL import ImageTk, Image

#### Globals
NRM = "normal"
VRT = "vertical"
HOR = "horizontal"

class Playground:
    ##### Playground class, duhh
    
    def __init__(self, master) -> None:
        ##### Init
        
        ##### Save the reference to master
        self.master = master

        ##### Ah, yes, this too
        self.isPressed = False
        self.mode = NRM

        ##### Make and Pack the import button
        self.btn_import = tk.Button(master, text="Import", command=self.import_)
        self.btn_import.configure(font=("Arial", 15), width=17, bg="#1f1f1f", fg="#f0f0f0")
        self.btn_import.pack()
        
    def resize(self, img):
        #### This function resizes the original object which is passed!

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        width, height = img.size

        if width>height and width > 0.8*screen_width:
            new_width = 0.8*screen_width
            new_height = new_width * height / width
        elif height > 0.8*screen_height:
            new_height = 0.8*screen_height
            new_width = new_height * width / height
        else:
            new_width = width
            new_height = height
            self.resizefactor = new_width/width
            return height, width, img
        
        self.resizefactor = new_width/width
        #### I think ANTIALIAS keeps the quality of the image. otherwise performance. not sure
        img = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)

        # check if resize is neccesary and return resized PIL Image object
        return new_height, new_width, img
        
        
    def import_(self):
        ##### Get filepath
        filepath = askopenfilename(
            filetypes=[("Image Files", "*.png"),
                        ("Image Files", "*.jpg"),
                        ("Image Files", "*.jpeg"),
                        ("All Files", "*.*")]
        )
        if not filepath:
            return
        ##### save reference to filefapth
        self.img_path = filepath

        ##### Get rid of old import button.
        self.btn_import.destroy()
        self.master.configure(padx=5, pady=5)

        ##### Make tk_img object with resized size and keep its reference
        self.resized_height, self.resized_width, resized_img = self.resize(Image.open(filepath))
        self.tk_img = ImageTk.PhotoImage(resized_img)

        ##### Make a canvas with same dimentions as of resizeed image and draw image on it
        self.canvas = tk.Canvas(self.master, width=self.resized_width, height=self.resized_height)
        self.canvas.bind("<Motion>", self.motion)
        self.canvas.bind("<Button-1>", self.buttonPressed)
        self.canvas.bind("<ButtonRelease-1>", self.buttonReleased)
        self.canvas.create_image((0, 0), image=self.tk_img, anchor='nw')
        self.canvas.pack()
        ##### End of function

    #### Takes a image and exports
    def export(self, cropped):
        filepath = asksaveasfilename(
            defaultextension="png",
            filetypes=[("Image Files", "*.png"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        cropped.save(filepath)
        return filepath

    #### Takes a box and updates the canvas
    def updatecanvas(self, x0, y0, x, y):
        #### https://stackoverflow.com/questions/54637795/how-to-make-a-tkinter-canvas-rectangle-transparent/54645103

        #### Set canvas background to the image
        self.canvas.create_image((0, 0), image=self.tk_img, anchor='nw')
        
        ##### Depending on state
        #### Set color
        #### Draw line
        #### Make and draw a box
        if self.mode == NRM:
            line_color = "#2fff00"
            self.canvas.create_line(x0, y0, x0, y, x, y, x, y0, x0, y0, fill=line_color, width=1)
            temp = Image.new("RGBA", (abs(x-x0), abs(y-y0)), line_color)
            temp.putalpha(50)
            self.temp_img = ImageTk.PhotoImage(temp)
            self.canvas.create_image((min(x,x0), min(y,y0)), image=self.temp_img, anchor='nw')
        else:
            line_color = "red"
        
        if self.mode == VRT:
            self.canvas.create_line(x0, 1, x0, self.resized_height-1, x, self.resized_height-1, x, 1, x0, 1, fill=line_color, width=1)
            temp = Image.new("RGBA", (abs(x-x0), int(self.resized_height)), line_color)
            temp.putalpha(50)
            self.temp_img = ImageTk.PhotoImage(temp)
            self.canvas.create_image((min(x,x0), 0), image=self.temp_img, anchor='nw')
        elif self.mode == HOR:
            self.canvas.create_line(1, y0, self.resized_width-1, y0, self.resized_width-1, y, 1, y, 1, y0, fill=line_color, width=1)
            temp = Image.new("RGBA", (int(self.resized_width), abs(y-y0)), line_color)
            temp.putalpha(50)
            self.temp_img = ImageTk.PhotoImage(temp)
            self.canvas.create_image((0, min(y,y0)), image=self.temp_img, anchor='nw')

    #### Motion of mouse event handler
    def motion(self, event):
        if self.isPressed:
            self.updatecanvas(self.buttonpressedeventinfo[0], self.buttonpressedeventinfo[1], event.x, event.y)

    #### Mouse pressed event handler
    def buttonPressed(self, event):
        self.buttonpressedeventinfo = [event.x, event.y]
        self.isPressed = True
        self.updatecanvas(self.buttonpressedeventinfo[0], self.buttonpressedeventinfo[1], event.x, event.y)

    #### Mouse released event handler
    def buttonReleased(self, event):
        self.isPressed = False
        left = min(self.buttonpressedeventinfo[0], event.x)
        right = max(self.buttonpressedeventinfo[0], event.x)
        top = min(self.buttonpressedeventinfo[1], event.y)
        bottom = max(self.buttonpressedeventinfo[1], event.y)
        
        self.box = (left / self.resizefactor, top / self.resizefactor, right / self.resizefactor, bottom / self.resizefactor)
        map(int, self.box)
        del self.buttonpressedeventinfo

    #### Enter key event handler
    def keyPressed(self, event):
        try:
            a,b,c,d = self.box
            if a == c or b == d:
                return
        except Exception:
            return
        
        #### The original non resized image
        img = Image.open(self.img_path)


        #### Normal cropping
        if self.mode == NRM:
            cropped =img.crop((self.box[0], self.box[1], self.box[2], self.box[3]))

        
        #### Vertical cropping
        if self.mode == VRT:
            im1 = img.crop((0, 0, self.box[0], img.height))
            im2 = img.crop((self.box[2], 0, img.width, img.height))
            cropped = Image.new("RGB", (im1.width + im2.width, img.height))
            cropped.paste(im1, (0, 0))
            cropped.paste(im2, (im1.width, 0))

        
        #### Horizontal cropping
        if self.mode == HOR:
            im1 = img.crop((0, 0, img.width, self.box[1]))
            im2 = img.crop((0, self.box[3], img.width, img.height))
            cropped = Image.new("RGB", (img.width, im1.height + im2.height))
            cropped.paste(im1, (0, 0))
            cropped.paste(im2, (0, im1.height))

        #### Export the cropped image
        filepath = self.export(cropped)
        if not filepath == None:
            messagebox.showinfo("Success", "Your image is successfuly exported to " + filepath)

    #### Called when mode is changed from Toolbar
    def reset(self):
        try:
            del self.box
            self.updatecanvas(0,0,0,0)
        except Exception:
            pass