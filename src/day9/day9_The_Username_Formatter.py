import pandas as pd
usernames= pd.Series(
    [' Alice ', 'bOB', ' Charlie_Data ', 'daisy']
)
usernames=usernames.str.strip()
usernames=usernames.str.lower()
print(usernames)
print("Usernames which as the letter a")
print(usernames.str.contains('a'))

