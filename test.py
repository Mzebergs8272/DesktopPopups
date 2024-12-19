from tkinter import Tk, Label, Toplevel
from PIL import ImageTk, Image
import json
import threading
from img_appender import Img_appender, add_img_data, rescale_img
import os
from keyboard import is_pressed
from random import choice
import pyautogui

_window = None
def toplevel(root=None):
    global _window
    _window = Toplevel()

    _window.geometry(f"{int(500)}x{int(100)}")
    _window.title("mefefef")

    _window.overrideredirect(False)

def check_pos(window: Toplevel):
    print(window.winfo_height())
    root.after(10, lambda: check_pos(window))


root = Tk()
root.geometry("1x1")
# root.overrideredirect(True)
threading.Thread(target=toplevel, daemon=True).start()

threading.Thread(target=lambda: root.after(1000, lambda: check_pos(_window)), daemon=True).start()

    

root.mainloop()
