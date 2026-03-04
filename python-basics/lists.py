# Name : Angela Amani
# Date : 18/02/2026
# Program to show lists in python
# list of friends
friends = ["Alice", "Bob", "Charlie", "David", "Frank","Eve"]

print(friends)
friends.sort() 
print(friends)
friends.reverse()
print(friends)
friends.append("Grace")
print(friends)

new_friends = ["Tracey", "Oscar", "Peggy", "Trent", "Victor", "Walter", "Xavier", "Yvonne", "Zara"]
print(len(new_friends))


# New list of students
students = friends + new_friends

print(students)
students.pop()
print(students)
students.insert(5, "Heidi")
print(students)
students.extend("Amani")
print(students)
students.remove("David")
print(students)

new_students = students.copy()
print(new_students) 