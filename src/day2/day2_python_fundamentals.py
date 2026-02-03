name = input("Enter your name ")
age = input("Enter your age ")
current_year = 2026
check_year = 2030
age= int(age)
modified_age=age+(check_year-current_year)
print("Hey",name,"you will be",modified_age,"years old in 2030!")

print("-------------------------------------------------------------------")

totle_amt = input("Enter your Totle Amount: ")
no_people = input("Enter number of people in share: ")
totle_amt=int(totle_amt)
no_people=int(no_people)
split_per_person= totle_amt/no_people
print("Share per Person (Bill / People)")
print("Total Bill:",totle_amt," . Each person pays:",split_per_person)
print(type(split_per_person))

print("-------------------------------------------------------------------")

item_name ="Watch"
quantity = 2
price = 4598.89
in_stock =True
print("Item:",item_name," Qty:", quantity," Price: ",price, "Available: ",in_stock)
totle_cost=(quantity * price)
print("Total cost:",totle_cost)