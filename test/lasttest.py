from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame or window
win= Tk()

# Set the size of the window
win.geometry("700x350")

# Set the title of the window
win.title("Combobox- TutorialsPoint")

# Update the Entry widget with the selected item in list
def check(e):
   v= entry.get()
      if v=='':
      data= values
   else:
      data=[]
      for item in values:
         if v.lower() in item.lower():
            data.append(item)
   update(data)

def update(data):
   # Clear the Combobox
   menu.delete(0, END)
   # Add values to the combobox
   for value in data:
      menu.insert(END,value)


# Add a Label widget
label= Label(win, text= "Demo Combobox Widget", font= ('Helvetica 15
bold'), background= "green3")
label.pack(padx= 10, pady= 25)

# Add a Bottom Label
text= Label(win, text="Select a Programming Language")
text.pack(padx= 15,pady= 20)

# Create an Entry widget
entry= Entry(win, width= 35)
entry.pack()
entry.bind('<KeyRelease>',check)

# Create a Listbox widget to display the list of items
menu= Listbox(win)
menu.pack()

# Create a list of all the menu items
values= ['Python', 'C++', 'Java','Ruby on Rails', 'Rust',
'GoLang','Objective-C', 'C# ', 'PHP', 'Swift', 'JavaScript']

# Add values to our combobox
update(values)

# Binding the combobox onclick

win.mainloop()