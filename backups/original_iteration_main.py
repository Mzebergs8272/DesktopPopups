from tkinter import Tk, Label, Toplevel, BooleanVar
from PIL import ImageTk, Image
import json
from backups.add_image import *
import threading
import keyboard as kb



class Popup:
    def __init__(self, image_data, position):
        self.image_data = image_data
        self._window = None
        self._img = None
        self._photo = None
        self.position = position

    def create(self):
        self._window = Toplevel()
        self._img = resize(Image.open(self.image_data["img_path"]), width=self.image_data["size"][0])
        self._window.geometry(f"{int(self._img.width)}x{int(self._img.height)}+{self.position[0]}+{self.position[1]}")
        self._window.title(self.image_data["number"])

        try:
            self._photo = ImageTk.PhotoImage(self._img)
            lbl = Label(self._window, text=self.image_data["number"], image=self._photo)
            lbl.image = self._photo
            lbl.pack()
        except Exception:
            pass

        self._window.mainloop()



def launch_popups(img_json_data: str):
    with open(img_json_data, "r") as f:
        data = json.load(f)
        threads = []    # need to be saved in memory because their variables are overwritten by eachother in for loop below
        popups: list[Popup] = []
        # min x pos: 775
        # max y pos: 1000
        valid_x_positions = [775, 775+310, 775+620]
        x = 0

        for i in range(len(data)):
            column_space_used = 0
            for popup in popups:
                if popup.position[0] == valid_x_positions[x]:
                    column_space_used += popup.image_data["size"][1] + 5
            print(column_space_used)
            if column_space_used + data[i]["size"][1] > 1060:
                print("not enogh column space")
                i -= 1
                x += 1
            else:
                popup = Popup(image_data=data[i], position=[valid_x_positions[x], 10])
                thread = threading.Thread(target=popup.create)

                thread.start()
                threads.append(thread)
                popups.append(popup)
                x += 1
                if x > 2: x = 0

def image_appender():
    root = Tk()
    root.geometry("500x500")
    focus_check = BooleanVar()
    Button(root, command=lambda: img_from_clipboard(root), text="paste image").pack()
    print(focus_check.get())
    if focus_check.get():
        print("fieof")
        kb.add_hotkey("ctrl+V", lambda: img_from_clipboard(root))


    root.bind('<FocusIn>', lambda _: focus_check.set(True))     # ' FIXME
    root.bind('<FocusOut>', lambda _: focus_check.set(False))
    root.mainloop()
    

if __name__ == "__main__":

    root = Tk()  # this root is here because when using toplevel tk object, its first instance of a popup is instead a default window, so i make this the default win
    root.geometry("1x1+-100+-100")    # positions window out of screen bounds
    
    # root.withdraw() # hides window
    
    launch_popups("data.json")
    # image_appender()
    

    root.mainloop()
