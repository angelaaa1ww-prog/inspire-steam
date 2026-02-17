# Name : AngeLa Amani
# Date :13/02/2026
# program to print the sin, cos and tan of angles from -180 to 180 with a step of 30 degrees


import math
for x in range(-180,180,30):
    print(math.sin(x), math.cos(x), math.tan(x))

import math

# Header
print("-----------------------------------------------")
print("| Degrees |    Sin    |    Cos    |    Tan    |")
print("-----------------------------------------------")

# Rows
for x in range(-180, 181, 30):
    print(f"| {x:7} | {math.sin(x):9.3f} | {math.cos(x):9.3f} | {math.tan(x):9.3f} |")

print("+----------------------------------------------")

    

  