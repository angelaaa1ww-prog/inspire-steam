# Name : Angela Amani
# Date : 19/02/2026
# Program to demonstrate the use of functions in Python

def cook_egg():
    oil = "20ml"
    pan = True
    moto = True
    eggs = 2
    print(f"The pan is {pan},and the fire is {moto},and the amount of oil is {oil} and cook {eggs} eggs")

print("Here is statement 1")

print("Here is statement 2")

cook_egg()

print("Here is statement 3")

# Ride_fare creating function

def create_fare(route, distance, is_rush_hour = True):

    fare = distance * 10
    if is_rush_hour==True:
        fare  = fare * 1.5
    print(f"The fare on route {route} is, {fare}")

    return fare
rush_hour = True
returned_fare = create_fare("Juja-Allsops", 7)
print(f"The fare returned is {returned_fare}")

# Passing a lidt as a parameter
def write_all_interests(interests):
     for interest in interests:
        print(f"I am interested in {interest}")

all_interests = ["Bike riding", "Hicking", "Traveling", "Coding"]

write_all_interests(all_interests)
    
