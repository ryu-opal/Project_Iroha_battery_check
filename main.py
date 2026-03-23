import psutil
import time
import os 
import sys 

import winsound
import threading
from plyer import notification
import pystray
from PIL import Image

BATTERY_CHARGE = 80 
LOW_BATTERY_LIMIT = 20 

def get_resource_path(relative_path): 
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

icon_path = get_resource_path("Iroha_icon.ico")
tray_icon_path = get_resource_path("Kaguya_icon.ico")

BATTERY_TITLE = "battery message" 

def check_battery():

    battery = psutil.sensors_battery()

    if battery is None:
        return False 

    percent = battery.percent
    plugged = battery.power_plugged

    if percent >= BATTERY_CHARGE and plugged:
        notification.notify(
            title=BATTERY_TITLE,
            message=f"The battery now is {percent}% , can unplug the charger", 
            app_icon=icon_path, 
            timeout=10 
        )
        return True 
    elif percent <= LOW_BATTERY_LIMIT and not plugged:
        notification.notify(
            title=BATTERY_TITLE,
            message=f"The battery now is {percent}%, , need to charge", 
            app_icon=icon_path, 
            timeout=10
        )
        winsound.Beep(500, 1000) 
        return True
    return False 

def monitor_loop(icon):
    while True:
        if check_battery(): 
            winsound.Beep(1000, 500) 
        time.sleep(300) 


def setup_icon():

    image = Image.open(tray_icon_path)
    
    menu = pystray.Menu(pystray.MenuItem("LEAVE", lambda icon, item: icon.stop()))
    icon = pystray.Icon("battery_monitor", image, "BATTERY CHECKER", menu)
    
    threading.Thread(target=monitor_loop, args=(icon,), daemon=True).start()
    icon.run()

if __name__ == "__main__":
    setup_icon() 
