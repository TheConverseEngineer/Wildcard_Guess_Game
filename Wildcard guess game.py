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
        self.Visuals.LevelMenu.CloseLevelMenu()
    
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
            
            def CreateLevelButton(self, x, y, num, Locked, **kwargs):
                round_rect(x, y, x+50, y+50, fill='#55666F', **kwargs)
                canvas.create_text(x+25, y+25, text = num, font=('Helvetica', 15), **kwargs)
                if Locked == True:
                    canvas.create_text(x+25, y+65, text = 'Locked', font=('Helvetica', 15), **kwargs)
                else: canvas.create_text(x+25, y+65, text = 'Unlocked', font=('Helvetica', 15), **kwargs)

                    

            def __init__(self):
                itemno = 0
                for i in range(2): #each row
                    for j in range(4): #each column
                        itemno += 1
                        if (itemno > MaxLevelUnlock): self.CreateLevelButton((100 * j) + 220,(125 * i) + 150, itemno, True, tag='LM')
                        else:
                            self.CreateLevelButton((100 * j) + 220,(125 * i) + 150, itemno, False, tags=('btn' + str(itemno), 'LM'))
                            canvas.tag_bind('btn' + str(itemno),"<Button-1>",Screens.Dynamics.LevelMenu.OpenLevel)
                #the last two
                if (9 > MaxLevelUnlock):
                    self.CreateLevelButton(220, 400, 9, True, tag='LM')
                else:
                    self.CreateLevelButton(220, 400, 9, False, tags=('btn9', 'LM'))
                    canvas.tag_bind('btn9' ,"<Button-1>",Screens.Dynamics.LevelMenu.OpenLevel)

                if (10 > MaxLevelUnlock):
                    self.CreateLevelButton(320, 400, 10, True, tag='LM')
                else:
                    self.CreateLevelButton(320, 400, 10, False, tags=('btn10', 'LM'))
                    canvas.tag_bind('btn10' ,"<Button-1>",Screens.Dynamics.LevelMenu.OpenLevel)      

            def CloseLevelMenu():
                for i in range(1, 17):
                    canvas.tag_unbind('btn'+str(i), "<Button-1>")
                canvas.delete('LM')
                
                

        class GameMode():
            LevelNumLabel = None
            TimeRemainingLabel = None
            hint = None
            def __init__(self):
                #globals
                global level
                global task
                global maxTask
                global time, e, f
                    
                #the labels
                self.LevelNumLabel = canvas.create_text(175, 115, text="Level %d, Task %d of %d" % (level, task, maxTask), font=('Helvetica', 20), fill='#2F1513', tags=('levnum', 'GameMode'))
                self.TimeRemainingLabel = canvas.create_text(625, 115, text="%d seconds remaining" % (time), font=('Helvetica', 20), fill='#2F1513', tags=('timeleft','GameMode'))
                self.hint = canvas.create_text(400, 470, text='Press me for a hint', font=('Helvetica', 16), fill='#2F1513', tags=('hint','GameMode'))
                
                #make entrybox
                e = tk.Entry(master, font="Helvetica 20 bold")
                canvas.create_window(400, 500, window=e, tag='GameMode')

                #make image
                Screens.Visuals.GameMode.CreateImage(level, task)
                
                #bind hint
                canvas.tag_bind('hint',"<Button-1>", self.Hint)

            def Hint(self, event):
                global level, task
                canvas.itemconfig('hint', text=LevelInfo.GetHint(level, task))
   
            def UpdateGUILabels(self):
                global level, task, maxTask, time
                canvas.itemconfig('levnum', text="Level %d, Task %d of %d" % (level, task, maxTask)) #update level num and task num
                canvas.itemconfig('timeleft', text="%d seconds remaining" % (time)) #update timer

            def CreateImage(lev, task):
                global CreatedImage
                print(lev, task)
                CreatedImage = Image.open(LevelInfo.GetPic(lev, task))
                w, h = CreatedImage.size
                CreatedImage = CreatedImage.resize((int(round((250 * int(w)) / int(h))), 250), Image.ANTIALIAS)
                CreatedImage = ImageTk.PhotoImage(CreatedImage)
                canvas.create_image(400, 300, image=CreatedImage, tags=('GameMode', 'QImg'))

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
                Screens.Visuals.StartScreen.Close(self)
                Screens.Visuals.LevelMenu()

            def PlayBtn(self):
                Screens.CloseAllScreens(Screens)
                Screens.Visuals.LevelMenu()
                
        class StartGameMode():

            def __init__(self):
                #globals
                global level, task, maxTask, EGMode, MaxLevelUnlock
                #set task to 1
                task = 1
                
                #trun off EGmode
                EGMode = False
                
                #get level info
                maxTask = LevelInfo.GetMaxTask(level)

                #Create screen
                Screens.Visuals.GameMode()

                for i in range(1, maxTask + 1):
                    self.InitTask(level, i)
                    if EGMode == True:
                        EGMode = False
                        return



                #close game mode
                Screens.CloseAllScreens(Screens)

                #see if new level was unlocked
                if level == MaxLevelUnlock:
                    MaxLevelUnlock += 1

                #open level menu
                Screens.Visuals.LevelMenu()
                    
            def InitTask(self, level, task):
                #globals
                global maxTime, TAns
                maxTime, TAns = LevelInfo.UnpackTask(task, level)
                canvas.delete('QImg')
                Screens.Visuals.GameMode.CreateImage(level, task)
                self.TaskGameLoop()
                canvas.itemconfig('hint', text="Press me for a hint")
                
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
                        return
                        
                    if time == 0: #if out of time
                        Screens.Visuals.GameMode.CreateJustText(False)
                        cor = True
                        task += 1
                        #close game mode
                        Screens.CloseAllScreens(Screens)

                        #open level menu
                        Screens.Visuals.LevelMenu()
                        
                    #update screen
                    Screens.Visuals.GameMode.UpdateGUILabels(Screens.Visuals.GameMode)

                    #update 
                    master.update()
                    master.update_idletasks()

        class LevelMenu():

            def OpenLevel(self):
                global level
                level = int(canvas.gettags(canvas.find_withtag("current"))[0][3])
                Screens.CloseAllScreens(Screens)
                Screens.Dynamics.StartGameMode()


                    
Screens.Visuals.StartScreen()
master.mainloop()
