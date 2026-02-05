raw_logs =["ID01", "ID02", "ID01", "ID05", "ID02", "ID08", "ID01"]
#Converting the lsit into sets

unique_users = set(raw_logs)

print(unique_users)

print("Is the id ID05 is unique ?",'ID05' in unique_users)

print(f"Number of entries in the original was {len(raw_logs)} reduced by {len(unique_users)} in totle \n{len(raw_logs)-len(unique_users)} was removed ")
