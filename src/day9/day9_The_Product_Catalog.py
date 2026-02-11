import pandas as pd

product= pd.Series([ 700, 150, 300],index=['Laptop', 'Mouse', 'Keyboard'])

print(product['Laptop'])
print("\n")
print(product[:2])
print("\n")
print(product)