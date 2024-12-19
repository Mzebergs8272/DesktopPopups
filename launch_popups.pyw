from tkinter import Tk, Label, Toplevel, Event
from PIL import ImageTk, Image
import json
import threading
from img_appender import Img_appender, add_img_data, rescale_img
import os
from keyboard import is_pressed
from random import choice
import pyautogui



# improved chatgpt iteration
# changed method of threading; created one background thread instead of one thread for each popup

script_dir = os.path.dirname(os.path.abspath(__file__)) # gets the absolute path of the directory of this file
os.chdir(script_dir)    # changes whatever direcetory this file is being run from to Image_Popups



class Popup:
    def __init__(self, image_data, position, number, root):
        self.number = number
        self.image_data = image_data
        self.position = position
        self._window = None
        self._img = None
        self._photo = None
        self.root = root

        # mouse pos relative to window
        self._window_mouse_pos = None 
        
    def launch(self):
        self._window = Toplevel()
        self._img = rescale_img(Image.open(self.image_data["img_path"]), width=self.image_data["size"][0])
        self._window.geometry(f"{int(self._img.width)}x{int(self._img.height)}+{self.position[0]}+{self.position[1]}")
        self._window.title(self.image_data["number"])
        self._window.resizable(False, False)

        # listens for left mouse button press
        self._window.bind("<ButtonPress-1>", self.update_window_mouse_pos)
        # if window is dragged, bind, passes Event object as arg into window_drag
        self._window.bind("<B1-Motion>", self.drag_window)
        
        self._window.overrideredirect(True)

        self._photo = ImageTk.PhotoImage(self._img)
        lbl = Label(self._window, text=self.image_data["number"], image=self._photo)
        lbl.image = self._photo  # Retain reference to prevent garbage collection
        lbl.pack()
        
    def get_position(self):
        return [self._window.winfo_x(), self._window.winfo_y()]

    def drag_window(self, event: Event):
        # places window on mouse position - pos of mouse while window was dragged. This drags the window from the position of mouse
        x = event.x_root - self._window_mouse_pos[0]
        y = event.y_root - self._window_mouse_pos[1]
        self._window.geometry(f"+{x}+{y}")
        # if overridedirect is false, then x position needs to be minused by additional height of title bar
    
    def update_window_mouse_pos(self, event: Event):
        # event.x and .y are mouse coords
        self._window_mouse_pos = [event.x, event.y]

            
class Popup_container:
    def __init__(self, root, img_json_path):
        self.popups: list[Popup] = []
        self.root = root
        self.img_json_path = img_json_path
        self.prev_json = None
        self.launched_popups = []

    def add_popup(self, img_json_obj: dict):
        added_popup = False
       

        if img_json_obj["position"]:
            position = img_json_obj["position"]
        else:
            position = [choice(range(0, 1800 - img_json_obj["size"][0], 50)), choice(range(0, 1030 - img_json_obj["size"][1], 50))] 

        popup = Popup(image_data=img_json_obj, position=position, number=int(img_json_obj["number"]), root=self.root)
        self.popups.append(popup)
        
        return added_popup

    def create_popups(self):
        data = self.get_img_data()
       
        for entry in data.values():
            if os.path.exists(os.path.join(os.getcwd(), f"images/img{entry["number"]}.png")):
               
                print("entry", entry)
                self.add_popup(entry)
    
    def check_for_esc(self):
        if is_pressed("ctrl+shift+alt+p"):exit()
        self.root.after(ms=1, func=self.check_for_esc)

    def launch_popups(self):

        if not self.prev_json: self.prev_json = self.get_img_data_str()

        if self.img_json_updated():
            new_data = self.get_img_data()
            
            for entry in new_data.values():
                
                if str(entry) not in json.loads(self.prev_json):
                    # print("added new popup")
                    self.add_popup(entry)
            
            self.prev_json = json.dumps(new_data)
        
        for popup in self.popups:
            if popup.image_data["number"] not in self.launched_popups and os.path.exists(popup.image_data["img_path"]):
                popup.launch()
                self.launched_popups.append(popup.image_data["number"])
            
        self.root.after(ms=100, func=self.launch_popups)
    
    def update_positions(self):
        data = self.get_img_data()
        for popup in self.popups:
            if popup._window is not None:
                pos = popup.get_position()
                data[str(popup.number)]["position"] = pos
                popup.position = pos
    
                add_img_data(self.img_json_path, {str(popup.number): data[str(popup.number)]})
        self.root.after(1000, self.update_positions)

    def get_img_data(self):
        with open(self.img_json_path, "r") as f:
            return json.load(f)

    def get_img_data_str(self) -> str:
        with open(self.img_json_path, "r") as f:
            data = json.load(f)
            return json.dumps(data)

    def img_json_updated(self) -> bool:
        if self.get_img_data_str() != self.prev_json:
            return True
        return False



run_image_appender = 0
run_popups = 1

# Initialize the root window
root = Tk()
# Position off-screen
root.geometry("1x1+-100+-100")
root.overrideredirect(True)

if run_popups:

    # Start the thread to instantiate popups and place in Popup_container.popups
    popup_container = Popup_container(root, "data.json")
    popup_container.create_popups()
    threading.Thread(target=popup_container.launch_popups, daemon=True).start()
    threading.Thread(target=popup_container.check_for_esc, daemon=True).start()
    threading.Thread(target=lambda: root.after(1000, popup_container.update_positions)).start()

if run_image_appender:
    img_appender = Img_appender("data.json")
    img_appender.run()

root.mainloop()
