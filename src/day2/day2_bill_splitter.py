totle_amt = input("Enter your Totle Amount: ")
no_people = input("Enter number of people in share: ")
totle_amt=int(totle_amt)
no_people=int(no_people)
split_per_person= totle_amt/no_people
print("Share per Person (Bill / People)")
print("Total Bill:",totle_amt," . Each person pays:",split_per_person)
print(type(split_per_person))