from tkinter import Tk, Label, Toplevel, BooleanVar, Button
from PIL import ImageTk, Image
import json
from backups.add_image import resize
import threading
import queue
from backups.add_image import img_from_clipboard
import keyboard as kb
import ctypes


class Popup:
    def __init__(self, image_data, position):
        self.image_data = image_data
        self.position = position
        self._window = None
        self._img = None
        self._photo = None

    def create(self):
        """
        GUI creation logic.
        """
        self._window = Toplevel()
        
        self._img = resize(Image.open(self.image_data["img_path"]), width=self.image_data["size"][0])
        self._window.geometry(f"{int(self._img.width)}x{int(self._img.height)}+{self.position[0]}+{self.position[1]}")
        self._window.title(self.image_data["number"])

        self._photo = ImageTk.PhotoImage(self._img)
        lbl = Label(self._window, text=self.image_data["number"], image=self._photo)
        lbl.image = self._photo  # Retain reference to prevent garbage collection
        lbl.pack()

        hwnd = ctypes.windll.user32.FindWindowW(None, self._window.title())
        


def launch_popups(img_json_data: str, command_queue: queue.Queue):
    """
    Load popup data and add creation commands to the queue.
    """
    with open(img_json_data, "r") as f:
        data = json.load(f)

    valid_x_positions = [775, 775 + 310, 775 + 620]
    x = 0
    popups: list[Popup] = []

    i = 0
    while i < len(data):
        column_space_used = sum(
            popup.image_data["size"][1] + 5
            for popup in popups
            if popup.position[0] == valid_x_positions[x]
        )
        
        print("col ", x, " space used ", column_space_used + data[i]["size"][1])
        if column_space_used + data[i]["size"][1] + 30 > 1060:
            i -= 1
        else:

            popup = Popup(image_data=data[i], position=[valid_x_positions[x], column_space_used])
            popups.append(popup)
            # Add the popup creation to the queue
            command_queue.put(popup)

        x = (x + 1) % len(valid_x_positions)    
        i += 1
        print(x)


def process_queue(command_queue: queue.Queue):
    """
    Process popup creation commands from the queue.
    """
    while not command_queue.empty():
        popup = command_queue.get()
        popup.create()  # Create the popup in the main thread
        

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

def set_z_position(hwnd):
    # Constants for SetWindowPos
    HWND_BOTTOM = 1
    SWP_NOACTIVATE = 0x0010
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001

    ctypes.windll.user32.SetWindowPos(hwnd, HWND_BOTTOM, 0, 0, 0, 0, SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE)

def get_popups_from_queue(queue: queue.Queue) -> list:
    popups = []

    while not queue.empty():
        popups.append(queue.get())
    
    return popups

# Initialize the root window
root = Tk()
root.geometry("1x1+-100+-100")  # Position off-screen

# Thread-safe queue for GUI commands
command_queue = queue.Queue()

# Start the thread to load data and schedule popups
threading.Thread(target=launch_popups, args=("data.json", command_queue), daemon=True).start()

# Periodically process commands from the queue
def check_queue():
    process_queue(command_queue)
    root.after(100, check_queue)

    for popup in get_popups_from_queue(command_queue):
        popup._window.after(100, lambda: set_z_position(popup._window))

check_queue()  # Start the queue processing loop
# image_appender()
root.mainloop()