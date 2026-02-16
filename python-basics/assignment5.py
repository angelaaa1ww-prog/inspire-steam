# Name : Angela Amani
# Date : 16/02/2024
# Program : To calculate oncpme tax

salary = int(input("Enter your gross salary: "))

if salary < 50000:
    tax = (2.5 * salary) / 100
    net_salary = salary - tax
    print(f"Your gross salary is: {salary}")
    print(f"Your net salary is: {net_salary}")
    print(f"Tax = {tax}")
elif salary >= 50000 and salary < 100000:
    tax = (4.5 * salary) / 100
    net_salary = salary - tax
    print(f"Your gross salary is: {salary}")
    print(f"Your net salary is: {net_salary}")
    print(f"Tax = {tax}")
elif salary >= 100000:
    tax = (7.5 * salary) / 100
    net_salary = salary - tax
    print(f"Your gross salary is: {salary}")
    print(f"Your net salary is: {net_salary}")
    print(f"Tax = {tax}")