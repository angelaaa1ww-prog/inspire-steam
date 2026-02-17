# Name : Amani Angela
# Date : 17/02/2026
# Program to display diamond and triangle

n = 5

for i in range(1,2*n):
    if i <= n:
        print(("*"*(2*i-1)).center(2*n-1))
    else:
        print(("*"*(2*(2*n-i)-1)).center(2*n-1))

# triangle display 

n = 5 #height 

for i in range(1,n+1):
    print(" "*(n-i) + "*" *(2*i-1))



a = int(input("enter a:"))
b = int(input("enter b:"))
c = int(input("enter c:"))

print(f"{a}x**2+{b}x+{c}=0")


