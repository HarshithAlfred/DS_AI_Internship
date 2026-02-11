import pandas as pd

scores= pd.Series(
    [85, None, 92, 45, None, 78, 55]
)
print("Students who where absent")
print(scores.isnull())
print("entering zero for nan")
scores= scores.fillna(0)
print(scores)
print("the score more than 60")
print(scores[ scores > 60])