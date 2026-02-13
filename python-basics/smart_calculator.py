# Name :: AngeLa Amani
# Date :1302/2026

# My smart calculator


def add(x, y):
    return x + y

def subtract(x, y):
    return(x - y)

def multiply(x, y):
    return(x * y)

def divide(x, y):
    if y==0:
        return "Error: Cannot be excecuted"
    return x / y

def calculator():
    print("Welcome to Amani's calculator!")
    while True:
        print("\nOptions: add, subtract, multiply, divide, quit")
        operation = input("Choose preffered operator: ").lower()

        if operation == "quit":
            print("Exiting calculator. Bye mwaah!")
            break

        if operation in ["add", "subtract", "multiply", "divide"]:
            try:
                x = float(input("Enter first number: "))
                y = float(input("Enter second number: "))
            except ValueError:
                print("Invalid input. Please enter numbers only.")
                continue

            if operation == "add":
                result = add(x, y)
            elif operation == "subtract":
                result = subtract(x, y)
            elif operation == "multiply":
                result = multiply(x, y)
            elif operation == "divide":
                result = divide(x, y)

            print(f"Result: {result}")
        else:
            print("Invalid operator. Please choose from add, subtract, multiply, divide, or quit.")


    

        






    


