"""*************************This is the storage for all the level information***********************************"""

MaxTime = [[10, 10, 10], [10, 10], [15], [15, 10], [18, 18], [20], [10], [25], [25], [25]]
Images = [['cat.jpg', 'water.jpg', 'clock.jpg'], ['sponge.png', 'mountain.jpg'], ['orange.jpg'], ['sunflower.jpg', 'kiwi.jpg'], ['Screw.jpg', 'Match.jpg'], ['pen.jpg'], ['cardboard.jpg'], ['cornFlake.jpg'], ['apple.jpg'], ['Knife.jpg']]
Ans = [['cat', 'water', 'clock'], ['sponge', 'mountain'], ['orange'], ['sunflower', 'kiwi'], ['Screw', 'Match'], ['pen'], ['cardboard'], ['corn flake']]
Hint = [['Meow', 'Splash!', 'Tick-tock'], ['soaks up water', 'tall'], ['peel and enjoy!'], ['bright yellow flower', 'also a type of bird'], ['holds stuff together', 'strike and burn'], ['fountain and ballpoint'], ['can be corrugated'], ['crunchy cereal made with corn'],['juicy and crunchy'], ['sharp']]
def UnpackTask(task, lev):
    return MaxTime[lev - 1][task - 1], Ans[lev - 1][task - 1]

def GetPic(lev, task):
    return ('Images/'+Images[lev - 1][task - 1])

def GetMaxTask(lev):
    return len(Ans[lev - 1])

def GetHint(lev, task):
    return Hint[lev - 1][task - 1]
