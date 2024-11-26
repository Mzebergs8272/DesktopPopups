from tkinter import Tk, Label, Toplevel
from PIL import ImageTk, Image
import json
from backups.add_image import rescale_img
import threading
from img_appender import Img_appender
import ctypes, os
from keyboard import is_pressed

# improved chatgpt iteration
# changed method of threading; created one background thread instead of one thread for each popup

script_dir = os.path.dirname(os.path.abspath(__file__)) # gets the absolute path of the directory of this file
os.chdir(script_dir)    # changes whatever direcetory this file is being run from to Image_Popups



class Popup:
    def __init__(self, image_data, position):
        self.image_data = image_data
        self.position = position
        self._window = None
        self._img = None
        self._photo = None

    def launch(self):
        self._window = Toplevel()
        self._img = rescale_img(Image.open(self.image_data["img_path"]), width=self.image_data["size"][0])
        self._window.geometry(f"{int(self._img.width)}x{int(self._img.height)}+{self.position[0]}+{self.position[1]}")
        self._window.title(self.image_data["number"])

        self._photo = ImageTk.PhotoImage(self._img)
        lbl = Label(self._window, text=self.image_data["number"], image=self._photo)
        lbl.image = self._photo  # Retain reference to prevent garbage collection
        lbl.pack()
        


class Popup_container:
    def __init__(self, root):
        self.popups: list[Popup] = []
        self.root = root

    
    def add_popup(self, img_json_data: dict):
        pass 
        # allow a popup to be appended to the background thread

        """
            copy, paste and redesign the create popups functionality by removing the entry_idx loop, then use this function in the create_popups function for every entry

            create a function that constantly checks for new json data in data.json and then runs this function

            how this will work

            user runs the launch popups programme
            user runs the img_appender programme and adds a new image to the json
            launch_popups detects json change, creates and displays a new popup
        """

    def create_popups(self, img_json_data: str):
        with open(img_json_data, "r") as f:
            data = json.load(f)

        # three columns (width 300) on right side of screen
        valid_x_positions = [775, 775 + 310, 775 + 620] 
        col_idx = 0
        entry_idx = 0
    
        while entry_idx < len(data):
        
            column_space_used = sum(popup.image_data["size"][1] + 5 for popup in self.popups if popup.position[0] == valid_x_positions[col_idx])
            
            # print("col ", col_idx, " space used ", column_space_used + data[entry_idx]["size"][1], "with", data[entry_idx])
            # if combined height of column popups and current popup > screen height - approx desktop nav height
            if column_space_used + data[entry_idx]["size"][1] > 1030: 
                
                # check if popup has space to fit on screen
                space_left_for_popup = False

                for i in range(3):
                    column_space_used = sum(popup.image_data["size"][1] + 5 for popup in self.popups if popup.position[0] == valid_x_positions[i])
                    if column_space_used + data[entry_idx]["size"][1] < 1030:
                        space_left_for_popup = True
                        break

                # use current entry in next iteration, next column because there is space left for curr popup on screen    
                if space_left_for_popup: entry_idx -= 1
                #else: print("can't fit ", data[entry_idx], "it takes up too much space |", "space used:", column_space_used + data[entry_idx]["size"][1], "max space: 1030")

            else:
                # instantiate popup, position is below other popups in current column
                popup = Popup(image_data=data[entry_idx], position=[valid_x_positions[col_idx], column_space_used])
                self.popups.append(popup)
                
            # rotates between columns
            col_idx = (col_idx + 1) % len(valid_x_positions)
            
            entry_idx += 1
    
    def check_for_esc(self):
        if is_pressed("ctrl+shift+alt+p"):
            exit()
        
        self.root.after(ms=1, func=self.check_for_esc)

    def launch_popups(self):
        for popup in self.popups:
            popup.launch()
            popup._window.overrideredirect(True)



# HWND_BOTTOM = 1
# SWP_NOACTIVATE = 0x0010
# SWP_NOMOVE = 0x0002
# SWP_NOSIZE = 0x0001

# def set_window_z_order(window):
     
#     hwnd = window.winfo_id()  # Get the window handle
#     ctypes.windll.user32.SetWindowPos(
#         hwnd,
#         HWND_BOTTOM,
#         0, 0, 0, 0,
#         SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE
#     )
    

# def lower_all_windows(root, popups):
#     # Lower the main Tk window
#     set_window_z_order(root)

#     # Lower all Toplevel windows
#     for popup in popups:
#         set_window_z_order(popup._window)
      

run_image_appender = 0
run_popups = 1


# Initialize the root window
root = Tk()
# Position off-screen
root.geometry("1x1+-100+-100")
root.overrideredirect(True)

if run_popups:

    # Start the thread to instantiate popups and place in Popup_container.popups
    popup_container = Popup_container(root)
    popup_container.create_popups("data.json")
    threading.Thread(target=popup_container.launch_popups, daemon=True).start()
    popup_container.check_for_esc()

if run_image_appender:
    img_appender = Img_appender("data.json")
    img_appender.run()

root.mainloop()
