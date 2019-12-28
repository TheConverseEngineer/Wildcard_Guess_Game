"""*************************This is the storage for all the level information***********************************"""

MaxTime = [[15, 15, 15], [15, 15, 15]]
Images = [['temp.jpg', 'temp.jpg', 'temp.jpg'], ['temp.jpg', 'temp.jpg', 'temp.jpg']]
Ans = [['cat', 'cat', 'cat'], ['cat', 'cat', 'cat']]

def UnpackTask(task, lev):
    return MaxTime[lev - 1][task - 1], Ans[lev - 1][task - 1]

def GetPic(task, lev):
        return ('Images/'+Images[lev - 1][task - 1])

def GetMaxTask(lev):
    return len(Ans[lev])
