import numpy as np

student_Score = np.random.randint(50,100,size=(5,3))

mean = np.mean(student_Score,axis=0)


normalization = (student_Score - mean)
print("The Original Score \n", student_Score)
print(" \n the Centerd Score \n",normalization)