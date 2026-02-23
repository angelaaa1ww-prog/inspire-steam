# Name : Angela Amani
# Date : 23/02/2026
# Program to classes in python

class Car():
    # attributes of the car
    def __init__(self, model, make, color, year):
        self.model = model 
        self.make = make
        self.color = color
        self.year = year

    # Printing the details of the car
    def detailss(self):
        print(f"The car is a {self.make} {self.model}  of color {self.color} was manufatured in the year {self.year}")



# instanciate a class object

my_car = Car("Camry", "Toyota", "Red", 2020)
dads_car = Car("Civic", "Honda", "Blue", 2018)

print(my_car.detailss())
print(dads_car.detailss())


