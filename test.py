import numpy as np

a = np.zeros((5, 2), dtype=np.long)

print(a)
a = np.insert(arr=a, obj=1, values=[1,1], axis=0)
print(a)