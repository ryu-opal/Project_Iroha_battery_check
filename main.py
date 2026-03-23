import psutil
import time
from plyer import notification

BATTERY_CHARGE = 50 

def check_battery():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        plugged = battery.power_plugged
        
        if percent >= BATTERY_CHARGE and plugged:
            notification.notify(
                title="battery notify",
                message=f"The battery now is {percent}% , can unplug the charger", 
                timeout=10
            )
            return True 
    return False 

print("battery check running...")
while True:
    if check_battery(): 
        time.sleep(300) 
    else:
        time.sleep(300) 

