# Name : Angela Amani
# Date : 11/02/2026
# Program to calculate  arithmetic progression

#calculate the nth term 

a = int(input("Enter the first number : "))
n = int(input("Enter the number of terms : "))
d = int(input("Enter the common difference : "))

nth_term = a + (n - 1) * d
print(f"The nth term is :{nth_term}")

sn = (n / 2) * (2 * a + (n - 1) * d)
print(f"The sum of the first n terms is : {sn}")




