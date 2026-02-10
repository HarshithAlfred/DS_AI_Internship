import numpy as np
flat_list= np.arange(24)
new_list = flat_list.reshape(4,3,2)

Transpose = np.transpose(new_list,(0,2,1))
print(new_list)
print(np.shape(new_list))
print(Transpose) 
print(np.shape(Transpose))