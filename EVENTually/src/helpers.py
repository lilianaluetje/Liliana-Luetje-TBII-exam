from PIL import Image, ImageTk
import tkinter as tk

def clear_widgets(root):
    for i in root.winfo_children():
        i.destroy()

def add_image(root, file_path, width, height):
    global pic, f1
    f1 = tk.Frame(root)
    img = Image.open(file_path)
    img = img.resize((width, height))
    pic = ImageTk.PhotoImage(img)
    Lab = tk.Label(f1, image=pic)
    Lab.pack()
    f1.pack()
    return f1  # Return the frame so it can be managed if needed
