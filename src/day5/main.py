from math_operations import power , avergae

if __name__=="__main__":
 base= int(input("Enter the base: "))
 exp= int(input("Enter the exponent: "))
 print(f"Power of base {base}, to exponent {exp} ",power(base,exp))

 num=[10, 20, 30, 40]
 print("averge of ",num ," is ",avergae(num))
