#Programe to generate number table from 1 to 100 using numpy arange function.

import numpy as np
n = int(input('Enter any number between 10 to 100:'))
for i in range(n):
    print(np.arange(start=i+1, stop=(i+1)*10+1, step=i+1), sep=' ')
