from tkinter import Tk, Label, Toplevel
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
        
    def launch(self):
        self._window = Toplevel()
        self._img = rescale_img(Image.open(self.image_data["img_path"]), width=self.image_data["size"][0])
        self._window.geometry(f"{int(self._img.width)}x{int(self._img.height)}+{self.position[0]}+{self.position[1]}")
        self._window.title(self.image_data["number"])

        # self._window.overrideredirect(False)

        self._photo = ImageTk.PhotoImage(self._img)
        lbl = Label(self._window, text=self.image_data["number"], image=self._photo)
        lbl.image = self._photo  # Retain reference to prevent garbage collection
        lbl.pack()
        
    def get_position(self):
        print(self._window)
        return self._window.winfo_x(), self._window.winfo_x()

    def can_drag(self):
        # pos = self.get_position()
        # if self._window.focus_get() and \
        # pos[0] < pyautogui.position()[0] < pos[0] + self._window.winfo_width() and \
        # pos[1] < pyautogui.position()[1] < pos[1] + self._window.winfo_height() and \
        # pyautogui.mouseDown():
        if self._window.focus_get():
            return True
        return False
            
            
            
class Popup_container:
    def __init__(self, root, img_json_path):
        self.popups: list[Popup] = []
        self.root = root
        self.img_json_path = img_json_path
        self.prev_json = None
        self.launched_popups = []

    def add_popup(self, img_json_obj: dict):
        added_popup = False
        # three columns (width 300) on right side of screen
        # valid_x_positions = [775, 775 + 310, 775 + 620] 
        # for pos in valid_x_positions:
        #     column_space_used = sum(popup.image_data["size"][1] + 5 for popup in self.popups if popup.position[0] == pos)
        #     if column_space_used + img_json_obj["size"][1] < 1030:
        #         popup = Popup(image_data=img_json_obj, position=[pos, column_space_used])
        #         self.popups.append(popup) 
        #         added_popup = True
        #         break

        if img_json_obj["position"]:
            position = img_json_obj["position"]
        else:
            position = [choice(range(0, 1920 - img_json_obj["size"][0], 50)), choice(range(0, 1030 - img_json_obj["size"][1], 50))] 

        popup = Popup(image_data=img_json_obj, position=position, number=int(img_json_obj["number"]), root=self.root)
        self.popups.append(popup)
        
        return added_popup

    def create_popups(self):
        data = self.get_img_data()
       
        for entry in data.values():
            if os.path.exists(os.path.join(os.getcwd(), f"images\img{entry["number"]}.png")):
               
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
                print("iter", entry)
                if str(entry) not in json.loads(self.prev_json):
                    print("added new popup")
                    self.add_popup(entry)
            
            self.prev_json = json.dumps(new_data)
        
        for popup in self.popups:
            if popup.image_data["number"] not in self.launched_popups:
                popup.launch()
                self.launched_popups.append(popup.image_data["number"])
            
        self.root.after(ms=100, func=self.launch_popups)
    
    def update_positions(self):
        data = self.get_img_data()
        for popup in self.popups:
            # print(popup)
            if popup._window is not None:
                data[str(popup.number)]["position"] = popup.get_position() 
                # print("updated position")
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
            print("img json updated")
            return True
        return False
    
    def check_popup_drag(self): 
        for popup in self.popups:
            if popup.can_drag():
                print("popup", popup.image_data["number"], "can drag")
            else:
                print("popup", popup.image_data["number"], "can't drag")

        self.root.after(1000, self.check_popup_drag)

        

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
    # popup_container.check_for_esc()
    threading.Thread(target=lambda: root.after(1000, popup_container.update_positions)).start()
    # root.after(1000, popup_coantainer.check_popup_drag)

if run_image_appender:
    img_appender = Img_appender("data.json")
    img_appender.run()

root.mainloop()
