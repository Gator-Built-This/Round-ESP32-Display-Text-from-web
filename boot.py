# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

#https://github.com/russhughes/gc9a01_mpy/tree/main 

import network
import vga1_bold_16x32 as font
import gc9a01
import tft_config
import time
import urequests
import ujson
import machine

# set up some variables with our wifi details, replace these with your Wi-Fi credentials
ssid = "xxxxxx"
password = "*******"

tft = tft_config.config(tft_config.TALL)


# this function connects the pico to a wifi network
def connect():
    #Sets up wireless module instance, turn on the wireless hardware, and then connect with our credentials
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    # We print the status of the connection here to help see whats going on
    while wlan.isconnected() == False:
        print("Connecting, please wait...")
        time.sleep(1)
    # Once it completes the while true loop, we will print out the Pico's IP on the network
    print("Connected! IP = ", wlan.ifconfig()[0])
    

def fetch_text_from_website(site):
    response = urequests.get(site)
    data = ujson.loads(response.text)
    response.close()
    return data['date'], data['time']

try:
    connect()
    # define the site we want to try to connect to
    site = "http://date.jsontest.com"
    print("Querying: ", site)
    # Query the site and store it in r, then we convert it from a JSON string
    
except OSError as e:
    # and if it fails, we will close the connection and let us know in the shell.
    r.close()
    print("Error: connection closed")

def main():

    tft.init()
    date_text, time_text = fetch_text_from_website(site)
    tft.rotation(0)
    tft.fill(0)
    fg = gc9a01.color565(255, 255, 255)
    bg = gc9a01.color565(0, 0, 0)
    for _ in range(128):
        tft.text(font, date_text, 50, 80, fg, bg) #syntax for this is #tft.text(font, whats is to be printed, column, row, foreground, background)
        tft.text(font, time_text, 40, 130, fg, bg) #syntax for this is #tft.text(font, whats is to be printed, column, row, foreground, background)
    time.sleep(10)
    tft.fill(0)
    machine.deepsleep()
main()
