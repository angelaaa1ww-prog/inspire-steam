# Name : Angela Amani
# Date : 12/02/2026
# Program to demonstrate the use of dictionaries in python

car = {
    "Model": "Audi",
    "Make": "Q8",
    "Color": "Cherry",
    "Year": 2025}
    
print(car)

print(car["Model"])
print(car["Year"])



students = dict(
                Alice=24,
                Bob=23,
                Charlie=22,
                David=21)
for key in students:
    print(key)

for val in students.values():
    print(val)
