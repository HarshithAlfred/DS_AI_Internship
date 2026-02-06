def calc_rectangle(length, width):
       area = length * width

       perimeter = 2 *(length+width)

       return area,perimeter

length = int(input("Enter the Length and Width of an Rectangle: "))
width = int(input())
area , perimeter= calc_rectangle(length,width)
print(f"Area {area}, Perimeter {perimeter}")

