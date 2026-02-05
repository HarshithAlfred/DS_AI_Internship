print("             Contact Book")
Contact={
    'John':893636483,
    'Tony':475837454,
    'Mark':984628374
}
print('\n')
print('Addition of the new Contact')
Contact['joel']=86837297
print('Updated Contact Book', Contact.items())
print('\n')
print("Contact ",Contact.get('John'))
print("Contact ",Contact.get('Fred'))
print('\n')
for Name,Number in Contact.items():
    print(F"Contact: {Name} | Phone: {Number}")