import tkinter as tk
from PIL import Image, ImageTk
import LevelInfo
import time as ProgTime

"""*************************Variables****************************"""
#State
state = 'Start'

#img var, to prevent trash
CreatedImage = None
#exit game mode
EGMode = False

#Level Number and Task Number
level, task, maxTask = 1, 1, 3

#task info
ImgName, TAns, maxTime = 0, 0, 0

#time remaining
time = 15

#max level unlocked
MaxLevelUnlock = 1
"""********************Starting Declarations**********************"""
#Master Entities
master = tk.Tk()

canvas = tk.Canvas(master, width = 800, height = 600, background='#B1B3B4')
canvas.pack()

#Permanent Entities
#Title
title = canvas.create_text(400, 50, font=('Helvetica', 35), fill='#2F1513',  text='Wildcard Guess Game', tag = 'title')

#Accessable entities
e = None
"""************************GUI Functions*************************"""
def round_rect(x1, y1, x2, y2, radius=25, **kwargs): #puts all corner points twice, starting at bottom of top left curve
    points = [x1, y1 + radius, #top left corner
              x1, y1 + radius,
              x1, y1,
              x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1, #top right corner
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius, #botton right corner
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2, #bottom left corner
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius]                                 
    return canvas.create_polygon(points, **kwargs, smooth=True)         

def CreateOnWindow(x, y, obj):
    return canvas.create_window(x, y, window = obj)

def MakeImage(x, y, source):
    load = Image.open(source)
    render = ImageTk.PhotoImage(load)
    img = canvas.create_image(x, y, image=render)
    img.image=render
    return img

"""***********************Screens*****************************"""
class Screens():

    def CloseAllScreens(self):
        self.Visuals.StartScreen.Close(self.Visuals.StartScreen)
        self.Visuals.GameMode.ExitGameMode()
    
    class Visuals(): #visuals

            
        class StartScreen():
            
            def __init__(self):
                #make the buttons
                #play button
                playBtn = round_rect(300, 200, 500, 300, radius = 25, fill='#018234', tags=('playBtnAction', 'StartScreen')) # play button
                playBtnText = canvas.create_text(400, 250, text='Play!', font = ('Helvetica', 30), tags=('playBtnAction', 'StartScreen'))
                canvas.tag_bind("playBtnAction","<Button-1>",Screens.Dynamics.StartScreen.PlayBtn)

                #Settings button
                setBtn = round_rect(300, 325, 500, 425, radius = 25, fill='#018234', tags=('setBtnAction', 'StartScreen'))
                setBtnText = canvas.create_text(400, 375, text='Options', font = ('Helvetica', 30), tags=('setBtnAction', 'StartScreen'))
                canvas.tag_bind("setBtnAction","<Button-1>",Screens.Dynamics.StartScreen.SettingsBtn)
                
            def Close(self):
                #unbind all buttons
                canvas.tag_unbind("playBtnAction", '<Button-1>')
                canvas.tag_unbind("setBtnAction", '<Button-1>')

                #destroy all entities
                canvas.delete('StartScreen')

        class LevelMenu():
            
            def CreateLevelButton(self, x, y, num, Locked):
                round_rect(x, y, x+50, y+50, fill='#55666F')
                canvas.create_text(x+25, y+25, text = num, font=('Helvetica', 15))
                if Locked == True:
                    canvas.create_text(x+25, y+65, text = 'Locked', font=('Helvetica', 15))
                else: canvas.create_text(x+25, y+65, text = 'Unlocked', font=('Helvetica', 15))

                    

            def __init__(self):
                itemno = 0
                for i in range(3): #each row
                    for j in range(4): #each column
                        itemno += 1
                        if (itemno > MaxLevelUnlock): self.CreateLevelButton((100 * j) + 220,(125 * i) + 150, itemno, True)
                        else: self.CreateLevelButton((100 * j) + 220,(125 * i) + 150, itemno, False)
                
                

        class GameMode():
            LevelNumLabel = None
            TimeRemainingLabel = None
            def __init__(self):
                #globals
                global level
                global task
                global maxTask
                global time, e
                    
                #the labels
                self.LevelNumLabel = canvas.create_text(175, 115, text="Level %d, Task %d of %d" % (level, task, maxTask), font=('Helvetica', 20), fill='#2F1513', tags=('levnum', 'GameMode'))
                self.TimeRemainingLabel = canvas.create_text(625, 115, text="%d seconds remaining" % (time), font=('Helvetica', 20), fill='#2F1513', tags=('timeleft','GameMode'))

                #make entrybox
                e = tk.Entry(master, font="Helvetica 20 bold")
                canvas.create_window(400, 500, window=e, tag='GameMode')

                #make image
                Screens.Visuals.GameMode.CreateImage(level, 1)

            def UpdateGUILabels(self):
                global level, task, maxTask, time
                canvas.itemconfig('levnum', text="Level %d, Task %d of %d" % (level, task, maxTask)) #update level num and task num
                canvas.itemconfig('timeleft', text="%d seconds remaining" % (time)) #update timer

            def CreateImage(lev, task):
                global CreatedImage
                CreatedImage = ImageTk.PhotoImage(Image.open(LevelInfo.GetPic(lev, task)))
                canvas.create_image(300, 300, image=CreatedImage, tag='GameMode')

            def CreateJustText(b):
                if b == True:
                    canvas.create_text(400, 550, text = 'Correct!', font=('Helvetica', 20), tags=('just', 'GameMode'))
                elif b == False:
                    canvas.create_text(400, 550, text = 'Time is up!', font=('Helvetica', 20), tag=('just', 'GameMode'))
                else: return
                master.update()
                master.update_idletasks()
                ProgTime.sleep(1)
                canvas.delete('just')

            def ExitGameMode():
                global EGMode
                EGMode = True #stop game loop
                canvas.delete('GameMode')
                
                
    class Dynamics(): #actions

        class StartScreen:

            def SettingsBtn(self):
                print('hi')
                Screens.Visuals.StartScreen.Close(self)
                Screens.Visuals.LevelMenu()

            def PlayBtn(self):
                print("Let's Play!")

        class StartGameMode():

            def __init__(self):
                #globals
                global level, task, maxTask, EGMode
                
                #get level info
                maxTask = LevelInfo.GetMaxTask(level)

                #Create screen
                Screens.Visuals.GameMode()

                #set task to 1
                task = 1
                for i in range(1, maxTask + 1):
                    print('a task')
                    self.InitTask(level, i)
                    if EGMode == True:
                        EGMode = False
                        return

                #close game mode
                Screens.CloseAllScreens(Screens)
                    
            def InitTask(self, level, task):
                #globals
                global maxTime, TAns
                maxTime, TAns = LevelInfo.UnpackTask(task, level)
                self.TaskGameLoop()
                
            def TaskGameLoop(self):
                global maxTime, time, TAns, e, task
                cor = False
                time = maxTime
                nextSec = ProgTime.time() + 1
                while (cor != True) and (time != 0):
                    
                    if ProgTime.time() >= nextSec: # run this code every second
                        nextSec = ProgTime.time() + 1
                        time -= 1
                        
                    if str(TAns).lower() in str(e.get()).lower(): #check if correct
                        Screens.Visuals.GameMode.CreateJustText(True)
                        cor = True
                        e.delete(0, len(e.get()))
                        task += 1
                        
                    if time == 0: #if out of time
                        Screens.Visuals.GameMode.CreateJustText(False)
                        cor = True
                        task += 1
                        #close game mode
                        Screens.CloseAllScreens(Screens)
                        
                    #update screen
                    Screens.Visuals.GameMode.UpdateGUILabels(Screens.Visuals.GameMode)

                    #update 
                    master.update()
                    master.update_idletasks()


                    
Screens.Visuals.LevelMenu()                    
master.mainloop()
