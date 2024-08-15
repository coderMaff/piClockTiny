#graphics pages for the tiny clock
from stellar import StellarUnicorn
from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN as DISPLAY

su = StellarUnicorn()
graphics = PicoGraphics(DISPLAY)

width = StellarUnicorn.WIDTH
height = StellarUnicorn.HEIGHT

# set up some pens to use later
PEN_ARROW = graphics.create_pen(40,100,40)
PEN_BACK = graphics.create_pen(0,0,30)
PEN_BLACK = graphics.create_pen(0, 0, 0)
PEN_BLUE = graphics.create_pen(0,70,110)
PEN_GREEN = graphics.create_pen(0,110,70)
PEN_GREY = graphics.create_pen(1,1,1)
PEN_RED = graphics.create_pen(110,0,70)
PEN_SAND = graphics.create_pen(100,100,0)
PEN_SEA = graphics.create_pen(25,25,100)
PEN_WHITE = graphics.create_pen(100,100,100)

###############################################################################

def checkButtons():
    if su.is_pressed(StellarUnicorn.SWITCH_BRIGHTNESS_UP):
        su.adjust_brightness(+0.01)
        last_second = None

    if su.is_pressed(StellarUnicorn.SWITCH_BRIGHTNESS_DOWN):
        su.adjust_brightness(-0.01)
        last_second = None

    return True

###############################################################################

def drawArrow(pFUp,pX):
    

    #Arrow
    graphics.set_pen(PEN_ARROW)
    graphics.rectangle(pX + 2,5,4,6)    
    
    if pFUp:
        graphics.rectangle(pX + 3,4,2,1)
        graphics.rectangle(pX + 1,6,6,1)        
    else:
        graphics.rectangle(pX + 3,11,2,1)
        graphics.rectangle(pX + 1,9,6,1)
        
    graphics.set_pen(PEN_BLACK)
    
    if pFUp:
        graphics.pixel( pX + 1,10)
        graphics.pixel( pX + 1, 9)
        graphics.pixel( pX + 1, 8)
        graphics.pixel( pX + 1, 7)
        graphics.pixel( pX + 0, 6)
        graphics.pixel( pX + 1, 5)
        graphics.pixel( pX + 2, 4)
        graphics.pixel( pX + 3, 3)
        graphics.pixel( pX + 4, 3)
        graphics.pixel( pX + 5, 4)
        graphics.pixel( pX + 6, 5)
        graphics.pixel( pX + 7, 6)        
        graphics.pixel( pX + 6, 7)
        graphics.pixel( pX + 6, 8)
        graphics.pixel( pX + 6, 9)
        graphics.pixel( pX + 6,10)
        graphics.pixel( pX + 5,11)
        graphics.pixel( pX + 4,11)
        graphics.pixel( pX + 3,11)
        graphics.pixel( pX + 2,11)        
    else:
        graphics.pixel( pX + 1,10)
        graphics.pixel( pX + 0, 9)
        graphics.pixel( pX + 1, 8)
        graphics.pixel( pX + 1, 7)
        graphics.pixel( pX + 1, 6)
        graphics.pixel( pX + 1, 5)
        graphics.pixel( pX + 2, 4)
        graphics.pixel( pX + 3, 4)
        graphics.pixel( pX + 4, 4)
        graphics.pixel( pX + 5, 4)
        graphics.pixel( pX + 6, 5)
        graphics.pixel( pX + 6, 6)        
        graphics.pixel( pX + 6, 7)
        graphics.pixel( pX + 6, 8)
        graphics.pixel( pX + 7, 9)
        graphics.pixel( pX + 6,10)
        graphics.pixel( pX + 5,11)
        graphics.pixel( pX + 4,12)
        graphics.pixel( pX + 3,12)
        graphics.pixel( pX + 2,11)
        
    return True

###############################################################################

def drawAurora(pAurora):    
           
    
    if pAurora < 3:
        graphics.set_pen(graphics.create_pen(112,198,52))
    elif pAurora == 3:
        graphics.set_pen(graphics.create_pen(40,126,58))
    elif pAurora == 4:
        graphics.set_pen(graphics.create_pen(253,253,91))
    elif pAurora == 5:
        graphics.set_pen(graphics.create_pen(202,182,111))
    elif pAurora == 6:
        graphics.set_pen(graphics.create_pen(234,62,72))
    elif pAurora == 7:
        graphics.set_pen(graphics.create_pen(139,54,74))
    elif pAurora == 8:
        graphics.set_pen(graphics.create_pen(158,150,222))
    elif pAurora == 9:
        graphics.set_pen(graphics.create_pen(110,81,189))
    
    graphics.rectangle(10,2,4,12)
    
    return True

###############################################################################

def drawBeach(pHeight,pFin):
    pHeight += 3
    pHeight *= 2
            
    graphics.set_pen(PEN_SAND)
    graphics.rectangle(8,0,16,16)
    
    graphics.set_pen(PEN_SEA)
    graphics.rectangle(8,16-int(pHeight),16,16)
    
    drawArrow(pFin,8)
            
    return True

###############################################################################

def drawClear():
    graphics.set_pen(PEN_GREY)
    graphics.clear()
    
    return True

###############################################################################

def drawGrid(pX, pY, pW, pData, pCol0 = PEN_BACK, pCol1 = PEN_RED, pCol2 = PEN_BLUE, pCol3 = PEN_GREEN, pCol4 = PEN_WHITE):
          
    x = 0
    y = 0
    l = 0
    while l < len(pData):
        if pData[l:l+1] == "1":
            graphics.set_pen(pCol1)
        elif pData[l:l+1] == "2":
            graphics.set_pen(pCol2)
        elif pData[l:l+1] == "3":
            graphics.set_pen(pCol3)
        elif pData[l:l+1] == "4":
            graphics.set_pen(pCol4)
        else:
            graphics.set_pen(pCol0)

        graphics.pixel(pX + x,pY + y)        
        x+=1
        l+=1
        if x % pW == 0:
            y+=1
            x=0
            
    return True

###############################################################################

def drawNumeral(pC,pX,pY,pColBack = PEN_BACK, pCol = PEN_WHITE):

    if pC == ".":
        drawGrid(pX,pY,1,"1",pColBack,pCol)
    elif pC == "0":
        drawGrid(pX,pY,3,"111101111",pColBack,pCol)
    elif pC == "1":
        drawGrid(pX,pY,3,"010010010",pColBack,pCol)
    elif pC == "2":
        drawGrid(pX,pY,3,"111000111",pColBack,pCol)                                                                 
    elif pC == "3":
        drawGrid(pX,pY,3,"111011111",pColBack,pCol)
    elif pC == "4":
        drawGrid(pX,pY,3,"100100111",pColBack,pCol)
    elif pC == "5":
        drawGrid(pX,pY,3,"101101010",pColBack,pCol)
    elif pC == "6":
        drawGrid(pX,pY,3,"100111111",pColBack,pCol)
    elif pC == "7":
        drawGrid(pX,pY,3,"111001010",pColBack,pCol)
    elif pC == "8":
        drawGrid(pX,pY,3,"111111111",pColBack,pCol)
    elif pC == "9":
        drawGrid(pX,pY,3,"111111001",pColBack,pCol)
    elif pC == ":":
        drawGrid(pX,pY,3,"010000010",pColBack,pCol)

    return True

###############################################################################
    
def drawTinySnake(pS,pC):    

    x = 0
    y = 0
    while x < pS:
        
        graphics.set_pen(pC)
        
        if x <= 15:
            graphics.pixel(x,0)
        if x > 15 and x < 31:
            graphics.pixel(15,x-15)
        if x > 30 and x < 46:
            if x == 31:
                y = 14
            graphics.pixel(y,15)
            y-=1
        if x > 45:
            if x == 46:
                y = 14
            graphics.pixel(0,y)
            y-=1            
        x+=1
        
    return True

###############################################################################

def drawUpdate():
    su.update(graphics)
    return True

###############################################################################

def drawWifiTime(pTime):
    drawNumeral(pTime[0:1],  0, 11, PEN_BACK, PEN_GREEN)
    drawNumeral(pTime[1:2],  3, 11, PEN_BACK, PEN_GREEN)
    drawNumeral(pTime[2:3], 10, 11, PEN_BACK, PEN_GREEN)
    drawNumeral(pTime[3:4], 13, 11, PEN_BACK, PEN_GREEN)    

    return True

###############################################################################
    
def drawWifi(pfDrawTime = False,pHour = 0, pMinute = 0):
    graphics.set_pen(PEN_BACK)
    graphics.clear()
    
    graphics.set_pen(PEN_WHITE)
    
    #Top Line
    graphics.rectangle(2,2,2,2)
    graphics.rectangle(4,1,8,2)
    graphics.rectangle(12,2,2,2)
        
    #Mid Line 1
    graphics.rectangle(4,6,2,2)
    graphics.rectangle(6,5,4,2)
    graphics.rectangle(10,6,2,2)
    
    #Mid Line 2
    graphics.rectangle(6,10,1,2)
    graphics.rectangle(7,9,2,2)
    graphics.rectangle(9,10,1,2)
    
    #Bottom Line
    graphics.rectangle(7,14,2,2)
    
    if pfDrawTime:
        drawWifiTime("{:02}{:02}".format(pHour, pMinute))        
        
    return True