print("Welcome to game play")
screen_res= 1920,1080
print("Current resolution",screen_res[0],"X",screen_res[1])
#trying to update the screen_res[0]
print("Tuples cannot be modified!")
screen_res[0]=1280
#TypeError: 'tuple' object does not support item assignment
