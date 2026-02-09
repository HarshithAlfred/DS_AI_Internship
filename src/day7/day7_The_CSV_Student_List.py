import csv
with open("student.csv","w") as file:
    writter = csv.writer(file)
    writter.writerow(['Name','Grade','Status'])
    writter.writerow(['Alice','A','Pass'])
    writter.writerow(['Bob','B','Pass'])
    writter.writerow(['Charlie','F','Fail'])

with open("student.csv","r") as file:
    reader = csv.DictReader(file)


    for line in reader:
        if line['Status']=='Pass':
           print(line)

