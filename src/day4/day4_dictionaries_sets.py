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

print('-------------------------------------------------')
raw_logs =["ID01", "ID02", "ID01", "ID05", "ID02", "ID08", "ID01"]
#Converting the lsit into sets

unique_users = set(raw_logs)

print(unique_users)

print("Is the id ID05 is unique ?",'ID05' in unique_users)

print(f"Number of entries in the original was {len(raw_logs)} reduced by {len(unique_users)} in totle \n{len(raw_logs)-len(unique_users)} was removed ")

print('-------------------------------------------------')

print("          Recommandation System")
friend_a = {"Python", "Cooking", "Hiking", "Movies"}
friend_b = {"Hiking", "Gaming", "Photography", "Python"}

print(' Interaction :', friend_a|friend_b,'All Interset')
print(' Union :', friend_a|friend_b, ' Shared Interest')
print(' Diffrence :', friend_a-friend_b,' Unique form Friend A to friend B')
