file_name= input("Enter the file name  (e.g., config.txt) ")
try: 
  with open(file_name,'r') as file:
    content = file.read()
    print(content)
except FileNotFoundError:
  print("Oops! That file doesn't exist yet")