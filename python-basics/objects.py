# Name : Amani Angela
# Date : 19/02/2026
# Classes (Objects) in Python

class Human:
    # First we define the attributes of a human being
    type == "mammal"
    legs = 2
    Brain = True
    Warm_blooded = True
    city = "Nairobi"
    
    # We then create a constructor for the class obect
    # The constructor will be used to create copies of this class object
    def __init__(self, name, age):
        self.human_name = name
        self.human_age = age

    def tell_story(self): 
        print(F"Hello I am a {self.human_name} Here is my story")
        print("There was once a human being who lived in a small village. He was very kind and loved by everyone. One day, he decided to go on an adventure to explore the world. He traveled to many different places and met many interesting people. He learned a lot about different cultures and ways of life. Eventually, he returned to his village and shared his stories with everyone. He lived happily ever after.")

 # Creat the objects   
amani = Human("Amani", 20)
triza = Human("Triza", 25)

# Let the humans do things

amani.tell_story()
print("Amani's age is:", amani.human_age)

triza.city = "Mombasa"

print("Triza's location: ", triza.city)
print("Amani's location: ", amani.city)

