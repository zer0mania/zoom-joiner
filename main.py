from os import system

system("cls")
system("title Zoom Joiner / tg: zer0mania")

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pystyle import Colors, Colorate, Center, Box
import threading
import requests
import time
import json
import sys

data = {}

with open('config.json') as f:
    data = json.load(f)

api = data['api']
list = data['list']
default_video_capture_Device = data['media.default_video_capture_Device']
default_audio_capture_device = data['media.default_audio_capture_device']

def instance(name, audio_enabled):
    options = Options()
    
    options.add_argument("--window-size=800,600")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    if audio_enabled == False:
        options.add_argument("--mute-audio")
    if default_video_capture_Device != "":
        options.add_experimental_option("prefs", { \
            "media.default_video_capture_Device": default_video_capture_Device, 
        })
    if default_audio_capture_device != "":
        options.add_experimental_option("prefs", { \
            "media.default_audio_capture_device": default_audio_capture_device, 
        })

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(60)
    driver.get(zoomUrl)
    
    try:
        driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div[1]/button').click() #cookies popup
    except NoSuchElementException:
        pass

    driver.find_element(By.XPATH, '//*[@id="inputname"]').send_keys(name)
    driver.find_element(By.XPATH, '//*[@id="joinBtn"]').click()

    try:
        passcode
        driver.find_element(By.XPATH, '//*[@id="inputpasscode"]').send_keys(passcode)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/div/form/div/div[3]/div').click() #passcode
    except (NoSuchElementException, NameError):
        pass

    #WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="foot-bar"]')))

    while True:
        if audio_enabled:
            js = "document.title = 'Audio enabled';"
            driver.execute_script(js)
        time.sleep(1)

def start():
    print(Colorate.Horizontal(Colors.green_to_white, "│"))
    threads = []
    audio_enabled = True
    for i in range(int(instances)):
        try:
            name = names[i]
        except IndexError:
            print(Colorate.Horizontal(Colors.red_to_white, f"└───| Out of names"))
            return 1
        if audio_enabled:
            print(Colorate.Vertical(Colors.yellow_to_red, f"├─| Audio enabled on {name}"))
        print(Colorate.Horizontal(Colors.green_to_white, f"└───| Starting instance {i+1}"))
        t = threading.Thread(target=instance, args=(name, audio_enabled,), daemon=True)
        threads.append(t)
        t.start()
        audio_enabled = False

logo = '''
 _____                         __        _                  
/ _  / ___   ___  _ __ ___     \ \  ___ (_)_ __   ___ _ __  
\// / / _ \ / _ \| '_ ` _ \     \ \/ _ \| | '_ \ / _ \ '__| 
 / //\ (_) | (_) | | | | | | /\_/ / (_) | | | | |  __/ |    
/____/\___/ \___/|_| |_| |_| \___/ \___/|_|_| |_|\___|_|    

                       tg: @zer0mania          
'''

print(Colorate.Vertical(Colors.blue_to_white, Center.XCenter(logo)))

if list == "true" and api == "true":
    api = "true"
    list = "false"

if list == "true":
    print("\n")
    print(Colorate.Horizontal(Colors.black_to_white, Center.XCenter(Box.DoubleCube("    Using list    "))))
elif api == "true":
    print("\n")
    print(Colorate.Horizontal(Colors.black_to_white, Center.XCenter(Box.DoubleCube("    Using API    "))))

orgUrl = input(Colorate.Horizontal(Colors.green_to_white, "\n├| URL / Meeting ID > "))

if "zoom.us" not in orgUrl:
    passcode = input(Colorate.Horizontal(Colors.green_to_white, "├| Passcode (leave blank if none) > "))
    orgUrl = "https://us05web.zoom.us/j/" + orgUrl

elif "?pwd=" not in orgUrl:
    passcode = input(Colorate.Horizontal(Colors.green_to_white, "├| Passcode (leave blank if none) > "))

instances = int(input(Colorate.Horizontal(Colors.green_to_white, "├| Instances > ")))

zoomUrl = orgUrl.replace("/j/", "/wc/join/")

if list == "true":
    names = open("names.txt").read().splitlines()
elif api == "true":
    print(Colorate.Horizontal(Colors.blue_to_green, "│"))
    print(Colorate.Horizontal(Colors.blue_to_green, "├──| Generating Names.."))

    names = []

    for i in range(instances):
        raw_request = requests.get(f"https://namey.muffinlabs.com/name.json?count=1&with_surname=true&frequency=all")
        data = raw_request.text
        parse_json = json.loads(data)
        name = parse_json[0]
        names.append(name)
        print(Colorate.Horizontal(Colors.blue_to_white, f"├─[{i+1}]: {name}"))

start()
print("\nPress enter to exit")
input()
system("taskkill /F /IM chromedriver.exe /T")
quit()
