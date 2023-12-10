import numpy as np

a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
b = [5, 5, 5, 5, 5, 5, 5, 5, 5]

c = a, b
d = np.transpose(c)
print(d[1])
