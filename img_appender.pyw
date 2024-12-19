# apply changes made to img_appender.py, to img_appender.pyw or vice versa

from tkinter import Tk, Button, Label, BooleanVar, Text, END
from PIL import ImageTk, Image, ImageGrab
import json, keyboard as kb, os

script_dir = os.path.dirname(os.path.abspath(__file__)) # gets the absolute path of the directory of this file
os.chdir(script_dir)    # changes whatever direcetory this file is being run from to Image_Popups


def rescale_img(img: Image, width) -> Image:
    aspect_ratio = img.width / img.height
    return img.resize((width, int(width / aspect_ratio)))
    

# puts image data in data.json
def add_img_data(json_file: str, entry: dict):

    file_data = None

    with open(json_file, mode="r") as f:
        file_data = json.load(f)
    with open(json_file, mode="w") as f:
        file_data.update(entry)
        json.dump(file_data, f)



class Img_appender:
    def __init__(self, img_data_file):
        self._window = None
        self.img_data_file = img_data_file
        self.txt_image_width = None

    def run(self):
        window = Tk()
        window.geometry("500x500")
        # focus_check = BooleanVar()
        Button(window, command=self.save_img_from_clipboard, text="paste image").pack()

        self.txt_image_width = Text(window, height=2, width=5)
        self.txt_image_width.pack()

        # if focus_check.get():
        #     kb.add_hotkey("ctrl+V", self.save_img_from_clipboard)

        # window.bind('<FocusIn>', lambda _: focus_check.set(True))     # ' FIXME
        # window.bind('<FocusOut>', lambda _: focus_check.set(False))
        window.mainloop()
    
    def save_img_from_clipboard(self):

        img_data = None

        with open("data.json", "r") as f:
            if f.readable():
                img_data = json.load(f)

        i = 0
       
        if img_data: i = int(list(img_data.keys())[-1]) + 1

        img_path = fr"images\img{i}.png"
        img_saved = self.save_clipboard_img(img_path)

        inp = self.txt_image_width.get("1.0", END).strip()
        if inp and int(inp) > 250:
            img_width = int(self.txt_image_width.get("1.0", END))
        else: 
            img_width = 250

        entry = {str(i): {
                    "number": i,
                    "img_path": img_path,  
                    "size": [img_width, rescale_img(Image.open(img_path), 300).height],
                    "position": []
                }}
        
        if img_saved: 
            add_img_data(self.img_data_file, entry)
            print("saved image", entry)

            # img = resize(Image.open(img_path), 500)
            # lbl = Label(root, image=ImageTk.PhotoImage(img))
            # lbl.image = img                                       FIXME
            # lbl.pack()

    # saves image from clipboard to images folder
    def save_clipboard_img(self, img_path):
        img = ImageGrab.grabclipboard()

        if img:
            img.save(img_path)
            return True
        else: 
            print("Your clipboard has no image right now")
            return False
           


if __name__ == "__main__":
    img_appender = Img_appender("data.json")
    img_appender.run()