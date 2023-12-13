# System
import time
import datetime
import requests
import json
import platform
import webbrowser
import os
import pyautogui
import threading 

import GUI
from datetime import datetime

# Prüfen Internetverbindung
timeout = 5
try:
    request = requests.get('https://app.powerbi.com', timeout=timeout)
    print("WLAN erfolgreich geprüft - " + datetime.now().isoformat())
except (requests.ConnectionError, requests.Timeout) as exception:
    print("kein Internet! - " + datetime.now().isoformat())




# Arbeitszeit
def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]

def start_gui():
    GUI.GUI()
    
# Starten des Threads für die GUI
gui_thread = threading.Thread(target=start_gui)
gui_thread.start()

time.sleep(5)

# Vollbild mit Klick
print("Dashboard öffnen")
pyautogui.FAILSAFE = False  # Fehler Cursor Tracking
webbrowser.open('https://app.powerbi.com/groups/me/dashboards/6d041d20-836a-4a16-a5b1-5a38d9cf464c?chromeless=1')
time.sleep(10)
#pyautogui.hotkey('f11')
#time.sleep(30)
#pyautogui.click(1901, 44)  # Meldung Wiederherstellen weg
#pyautogui.click(1815, 1020)  # X/Y Koordinaten Breite anpassen

print('Loop gestartet. Drücke Ctrl-C um zu beenden.')
while True:
    try:         
        
        time.sleep(60)  # Prozess verzögern

        # Um Mitternach rebooten (falls gewünscht)
        betriebsdauer = abs(int(time.time()) - int(time.time())) / 3600
        rebootfenster = is_between(time.strftime('%H:%M', time.localtime()), ("00:00", "01:00"))
        if rebootfenster and betriebsdauer > 2:
            print("wird neu gestartet")
            time.sleep(2)
            os.system('sudo reboot')

    except Exception as err:
        print('Fehler: ' + str(err))
        Error = str(err)
        break

# Bei Internetverbindung Fehlermeldung absetzten
try:
    request = requests.get('http://www.google.ch', timeout=timeout)
    data = {"Datum": datetime.now().isoformat(), "Fehler": Error}
    response = requests.post(hook_url_hiag_error, data=json.dumps(data), headers={'Content-Type': 'application/json'})
except (requests.ConnectionError, requests.Timeout) as exception:
    print('keine Verbindung für Log Fehlermeldung')

# Falls Prozess unterbrochen wird neu starten
print('CPS wird in 10 min neu gestartet')
time.sleep(600)
os.system('sudo reboot')
