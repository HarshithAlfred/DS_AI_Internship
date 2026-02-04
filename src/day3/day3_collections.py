print("Welcome grocery store")
inventory= ["Apples", "Bananas", "Dates", "Carrots"]
print(inventory)
print("An new order of eggs added")
inventory.append("Eggs")
print("Updated Inventory")
print(inventory)
print("the Bananas has been soldout")
inventory.remove("Bananas")
print("Updated Inventory")
print(inventory)
print("Arranging of inventory")
inventory.sort()
print("Updated Inventory")
print(inventory)

print('--------------------------------------------')

temperatures = [22, 24, 25, 28, 30, 29, 27, 26, 24, 22]
print("Readings of temperature of every hour",temperatures)
print("Readings of hours in first ",temperatures[0]," and Readings of last ",temperatures[-1])
print("Afternoon Peak Reading",temperatures[3:6])
print("Reading of last 3 hours",temperatures[-3:])

print('--------------------------------------------')

print("Welcome to game play")
screen_res= 1920,1080
print("Current resolution",screen_res[0],"X",screen_res[1])
#trying to update the screen_res[0]
print("Tuples cannot be modified!")
screen_res[0]=1280
#TypeError: 'tuple' object does not support item assignment
