# maf 2024.08.06 Created
# maf 2024.08.15 Seperated GFX out to maphics.py
#
# tinyClock with extra info
# tide times
# aurora warning
# wifi connect

import time
import machine
import network
import ntptime
import requests
import maphics

from stellar import StellarUnicorn

try:
    from clockTiny_config import WIFI_SSID, WIFI_PASSWORD, URL_TIDETIME, URL_AURORA, URL_WEATHER
    wifi_available = True
except ImportError:
    print("Create clockTiny_config.py with your WiFi credentials and localised URLs")
    wifi_available = False

###############################################################################

def tinyAurora():
    global aurora
    if(aurora == ""): return
    
    maphics.drawAurora(int(aurora['locations']['karmoy']['kp']))

    return True
    
###############################################################################    

def tinyTide():
    
    global tides
    if(tides == ""): return
        
    maphics.drawBeach(tides['items'][0]['value'],tides['items'][0]['value'] > tides['items'][1]['value'])
                
    return True

###############################################################################            

def tinyTemp(pHour = 0):

    global weather
    if(weather == ""): return

    temp = weather['hourly']['temperature_2m'][pHour] * 10

    #print("Temp",weather['hourly']['temperature_2m'][pHour],temp)

    tempStr = "{:03}".format(temp)

    maphics.drawNumeral(tempStr[0:1], 11, 2, maphics.PEN_BLACK, maphics.PEN_RED)
    maphics.drawNumeral(tempStr[1:2], 11, 6, maphics.PEN_BLACK, maphics.PEN_RED)
    maphics.drawNumeral(tempStr[2:3], 11,10, maphics.PEN_BLACK, maphics.PEN_RED)
    maphics.drawNumeral(".", 9,12, maphics.PEN_BLACK, maphics.PEN_RED)

    return True

###############################################################################            
    
def tinyCloud(pX,pY):
    cloudText =  "01101100" 
    cloudText += "11111110"
    cloudText += "11111111"
    cloudText += "01110110"
    cloudText += "02002020"
    cloudText += "00020000"
    cloudText += "00200200"
    cloudText += "00000000"    
    cloudText += "02002000"    

    maphics.drawGrid(pX,pY,8,cloudText,maphics.PEN_BLACK, maphics.PEN_WHITE, maphics.PEN_BLUE)        

    return True

###############################################################################            

def tinyRain(pHour = 0):

    global weather
    if(weather == ""): return

    chance = weather['hourly']['precipitation_probability'][pHour] 

    #print("Temp",weather['hourly']['precipitation_probability'][pHour],chance)

    tempStr = "{:02}".format(chance)

    maphics.drawNumeral(tempStr[0:1],  9, 2, maphics.PEN_BLACK, maphics.PEN_BLUE)
    maphics.drawNumeral(tempStr[1:2], 12, 2, maphics.PEN_BLACK, maphics.PEN_BLUE)    

    tinyCloud(8,6)

    return True
            
###############################################################################            
    
def tinyHeart():
    heartText =  "0000000000000000" 
    heartText += "0001110000111000"
    heartText += "0011111001111100"
    heartText += "0111111111111110"
    heartText += "0112121111212110"
    heartText += "1112121221212111"
    heartText += "1112121111212111"
    heartText += "1112121221212111"
    heartText += "0112121111212110"
    heartText += "0111111111111110"
    heartText += "0011111111111100"
    heartText += "0011111111111100"
    heartText += "0001111111111000"
    heartText += "0000111111110000"
    heartText += "0000001111000000"
    heartText += "0000000110000000"
    
    maphics.drawGrid(0,0,16,heartText,maphics.PEN_BACK, maphics.PEN_RED, maphics.PEN_WHITE)        
###############################################################################        
            
def tinyClockDraw(pTime):    
    maphics.drawNumeral(pTime[0:1], 1,  2, maphics.PEN_BLACK, maphics.PEN_BLUE)
    maphics.drawNumeral(pTime[1:2], 4,  2, maphics.PEN_BLACK, maphics.PEN_BLUE)
    maphics.drawNumeral(pTime[2:3], 1,  6, maphics.PEN_BLACK, maphics.PEN_BLUE)
    maphics.drawNumeral(pTime[3:4], 4,  6, maphics.PEN_BLACK, maphics.PEN_BLUE)    
    maphics.drawNumeral(pTime[4:5], 1, 11, maphics.PEN_BLACK, maphics.PEN_BLUE)
    maphics.drawNumeral(pTime[5:6], 4, 11, maphics.PEN_BLACK, maphics.PEN_BLUE)
    
    maphics.drawNumeral(pTime[ 6: 7],  9,  2, maphics.PEN_BLACK, maphics.PEN_GREEN)
    maphics.drawNumeral(pTime[ 7: 8], 12,  2, maphics.PEN_BLACK, maphics.PEN_GREEN)
    maphics.drawNumeral(pTime[ 8: 9],  9,  6, maphics.PEN_BLACK, maphics.PEN_GREEN)
    maphics.drawNumeral(pTime[ 9:10], 12,  6, maphics.PEN_BLACK, maphics.PEN_GREEN)    
    maphics.drawNumeral(pTime[12:13],  9, 11, maphics.PEN_BLACK, maphics.PEN_GREEN)
    maphics.drawNumeral(pTime[13:14], 12, 11, maphics.PEN_BLACK, maphics.PEN_GREEN)    
    
###############################################################################
        
def sync():
    global tides, aurora, weather, hour, minute
    if not wifi_available:
        return

    # Start connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    # Wait for connect success or failure
    max_wait = 100
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(0.2)

        maphics.drawWifi(True,hour,minute)        
        maphics.drawUpdate()

    if max_wait > 0:
        print("Connected")

        try:            
            ntptime.settime()            
        
            response =requests.get(URL_AURORA)
            print('Response code: ', response.status_code)
            aurora = response.json()
            response.close()
            print('Aurora JSON:', aurora)
        
            response = requests.get(URL_TIDETIME)            
            print('Response code: ', response.status_code)                    
            tides = response.json()            
            response.close()
            print('Tide JSON: ', tides)

            response = requests.get(URL_WEATHER)            
            print('Response code: ', response.status_code)                    
            weather = response.json()            
            response.close()
            print('Weather JSON: ', weather)

        except OSError:
            pass

    wlan.disconnect()
    wlan.active(False)
    
    return True

###############################################################################
    
def adjust_utc_offset(pin):
    global utc_offset, last_second
    if pin == up_button:
        utc_offset += 1
        last_second = None
    if pin == down_button:
        utc_offset -= 1
        last_second = None

    return True

###############################################################################

def redraw_display_if_reqd():
    global year, month, day, wd, hour, minute, second, last_second, iType, last_minute, displayMode
    
    displayList = ["Date","Rain","Temp","Tide","Aurora"]    
    year, month, day, wd, hour, minute, second, _ = rtc.datetime()

    if minute != last_minute:
        iType+=1
        if iType >= len(displayList):
            iType = 0            
        displayMode = displayList[iType]        

    if second != last_second:        
        
        hour = (hour + utc_offset) % 24
        time_through_day = (((hour * 60) + minute) * 60) + second        
                
        if ( minute % 10 == 0 and second == 0 ) or tides == "" or aurora == "":
            sync()            
        
        maphics.drawClear()

        displayMode = "Temp"
    
        if (hour == 11 or hour == 23 ) and minute == 11:   
           tinyHeart()
        elif displayMode == "Rain":
            tinyRain(hour)
            maphics.drawTinySnake(second,maphics.PEN_RED)
            tinyClockDraw("{:02}{:02}{:02}".format(hour, minute, second, day, month, year))
        elif displayMode == "Temp":
            tinyTemp(hour)
            maphics.drawTinySnake(second,maphics.PEN_SAND)
            tinyClockDraw("{:02}{:02}{:02}".format(hour, minute, second, day, month, year))
        elif displayMode == "Tide":        
            tinyTide()
            maphics.drawTinySnake(second,maphics.PEN_GREEN)
            tinyClockDraw("{:02}{:02}{:02}".format(hour, minute, second, day, month, year))
        elif displayMode == "Aurora":
            tinyAurora()
            maphics.drawTinySnake(second,maphics.PEN_WHITE)
            tinyClockDraw("{:02}{:02}{:02}".format(hour, minute, second, day, month, year))        
        else:
            maphics.drawTinySnake(second,maphics.PEN_RED)
            tinyClockDraw("{:02}{:02}{:02}{:02}{:02}{:04}".format(hour, minute, second, day, month, year))        

            
    maphics.drawUpdate()
    last_second = second
    last_minute = minute
    
###############################################################################

# create the rtc object
rtc = machine.RTC()

#JSON objects
tides = ""
aurora = ""
weather = ""

#Variables
iType = 0
utc_offset = 1
last_second = 0
last_minute = 0
displayMode = ""

up_button = machine.Pin(StellarUnicorn.SWITCH_VOLUME_UP, machine.Pin.IN, machine.Pin.PULL_UP)
down_button = machine.Pin(StellarUnicorn.SWITCH_VOLUME_DOWN, machine.Pin.IN, machine.Pin.PULL_UP)

up_button.irq(trigger=machine.Pin.IRQ_FALLING, handler=adjust_utc_offset)
down_button.irq(trigger=machine.Pin.IRQ_FALLING, handler=adjust_utc_offset)

year, month, day, wd, hour, minute, second, _ = rtc.datetime()


sync()

while True:
    maphics.checkButtons()
                
    redraw_display_if_reqd()

    maphics.drawUpdate()
    # update the display
    time.sleep(0.01)
