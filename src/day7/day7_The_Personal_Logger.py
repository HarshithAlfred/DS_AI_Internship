name= input("Enter your name ")
goal=input("Enter your Goal ")
with open("sample.txt",'a') as file:
    file.write("name:"+name)
    file.write("Goal:"+goal+"\n")