from keyboard import is_pressed
from os import system
from threading import Thread
from psutil import process_iter

# finds if python3 is running and the script_name program is running inside
def find_python_program(script_name):
    for process in process_iter(['pid', 'name', 'cmdline']):    # iterates through all program processes
        if process.info['name'] == 'python' or process.info['name'] == 'python3':   # if python running
            cmdline = process.info['cmdline']                   # info contains specific python program names
            if cmdline and script_name in ' '.join(cmdline):    # if specified file in info
                return process.info['pid']
    return None

while True:
    if is_pressed("ctrl+shift+p") and not find_python_program("launch_popups.pyw"):
        Thread(target=lambda: system("pythonw launch_popups.pyw")).start() 