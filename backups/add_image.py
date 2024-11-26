from tkinter import Tk, Button, Label, BooleanVar
from PIL import ImageTk, Image, ImageGrab
import json, keyboard as kb

def rescale_img(img: Image, width) -> Image:
    aspect_ratio = img.width / img.height
    return img.resize((width, int(width / aspect_ratio)))

# puts image data in data.json
def append_img_data(file: str, entry: list[dict]):

    file_data = None

    with open(file, mode="r") as f:
        file_data = json.load(f)
        
    with open(file, mode="w") as f:
        json.dump(file_data + entry, f)

# saves image from clipboard to images folder
def save_clipboard_img(img_path):
    img = ImageGrab.grabclipboard()

    if img:
        img.save(img_path)
        return True
    else: 
        print("no image saved to clipboard")
        return False


def img_from_clipboard(root):

    img_data = None

    with open("data.json", "r") as f:
        if f.readable():
            img_data = json.load(f)

    i = 0
    if img_data: i = img_data[-1]["number"] + 1

    img_path = fr"images\img{i}.png"
    img_saved = save_clipboard_img(img_path)

    entry = [{
                "number": i,
                "img_path": img_path,  
                "size": [300, rescale_img(Image.open(img_path), 300).height]
            }]
    
    if img_saved: 
        append_img_data("data.json", entry)
        print("saved image", entry)

        # img = resize(Image.open(img_path), 500)
        # lbl = Label(root, image=ImageTk.PhotoImage(img))
        # lbl.image = img                                       FIXME
        # lbl.pack()

def image_appender():
    root = Tk()
    root.geometry("500x500")
    focus_check = BooleanVar()
    Button(root, command=lambda: img_from_clipboard(root), text="paste image").pack()
    print(focus_check.get())
    if focus_check.get():
        kb.add_hotkey("ctrl+V", lambda: img_from_clipboard(root))

    root.bind('<FocusIn>', lambda _: focus_check.set(True))     # ' FIXME
    root.bind('<FocusOut>', lambda _: focus_check.set(False))
    root.mainloop()


class Img_appender:
    def __init__(self):
        pass

    def run(self):
        pass

