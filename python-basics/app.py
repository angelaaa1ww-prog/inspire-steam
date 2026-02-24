from  tkinter import *

def Hello():
	print("Hello! from Amani")

root = Tk()
root.geometry("600x600")

frame_one = Frame(root)
frame_one.pack()
button_one = Button(frame_one, text="say hello!", command = Hello )
button_one.pack()
root.mainloop()





