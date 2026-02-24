# Name : Angela Amani
# Date : 24/02/2026
# Program to perform file operations in Python

# Create new file
new_file = open("student_data.txt", "r+")

# Write to new file
new_file.write("{Student Name: Amani Angela , ID : 22240331 , email :instrumental@gmail.com}")



# read new file
new_file = open("student_data.txt", "r")

data = new_file.read()

print(data)

new_file.close()

# Delete file
# use os module
import os
os.remove("remove.txt")


#Delete folder
os.rmdir("folder")





