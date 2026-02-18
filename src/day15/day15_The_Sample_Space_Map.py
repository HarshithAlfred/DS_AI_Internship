import random
trails = 1000000000
count=0
for t in range(trails):
    dice_A = random.randint(1,6)
    dice_B = random.randint(1,6)
    if (dice_A+dice_B)== 7:
        count+=1

print(count)

print(count/trails)