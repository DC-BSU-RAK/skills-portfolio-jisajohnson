from tkinter import *
from PIL import ImageTk
from tkinter import messagebox

main = Tk()
main.title("Student Manager")
main.geometry("750x550")
main.iconphoto(False, ImageTk.PhotoImage(file=r"Exercise 3\images\studentmanagerlogo.png"))
main.resizable(0, 0)
main.configure(bg='#2E0854')

#Purple color scheme for the UI and to make it visually appealing
COLORS = {
    'darkpurple': '#2E0854',
    'mediumdarkpurple': '#4B0082',
    'mediumpurple': '#9370DB',
    'lightpurple': '#D8BFD8',
    'lavender': '#E6E6FA',
    'violet': '#EE82EE',
    'brightpurple': '#8A2BE2',
    'textcolor': '#FFFFFF',
    'buttonbg': '#8A2BE2',
    'buttonfg': '#FFFFFF',
    'listboxbg': '#E6E6FA',
    'listboxfg': '#4B0082',
    'headerbg': '#6A0DAD',
    'accentcolor': '#DA70D6'
}
#To store student data
students = []

def loadstudentdata():
    """Load student data from the text file into the students list."""
    with open("Exercise 3/studentMarks.txt", "r") as f:
        lines = f.readlines()
        numstudents = int(lines[0].strip())
        for i in range(1, numstudents + 1):
            parts = lines[i].strip().split(",") #Split by comma to get individual data
            student = {
                "code": int(parts[0]),
                "name": parts[1],
                "cw1": int(parts[2]), #Using cw to represent coursework
                "cw2": int(parts[3]),
                "cw3": int(parts[4]),
                "exam": int(parts[5])
            }
            students.append(student)

def resultcalculation(student):
    """Calculate total coursework, total marks, percentage, and grade for a student."""
    totalcoursework = student["cw1"] + student["cw2"] + student["cw3"]
    total = totalcoursework + student["exam"] #Total marks out of 160
    percentage = (total / 160) * 100 #Calculate percentage
    #To determine grade based on percentage
    if percentage >= 70:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"

    return totalcoursework, percentage, grade

def studentview(student):
    """To get a proper formatted string of a student's details."""
    totalcoursework, percentage, grade = resultcalculation(student)
    return (f"Name: {student['name']}\n"
            f"Student Number: {student['code']}\n"
            f"Total Coursework: {totalcoursework}/60\n"
            f"Exam Mark: {student['exam']}/100\n"
            f"Percentage: {percentage:.1f}%\n"
            f"Grade: {grade}\n")

def clearoutput():
    """To clear the output text area."""
    outputtext.config(state=NORMAL)
    outputtext.delete(1.0, END)
    outputtext.config(state=DISABLED)

def studentsviewall():
    clearoutput()
    """To view all students and class average."""
    outputtext.config(state=NORMAL)
    outputtext.delete(1.0, END)
    totalpercentage = 0
    #To display each student's details
    for i, student in enumerate(students, 1):
        _, percentage, _ = resultcalculation(student)
        totalpercentage += percentage
        outputtext.insert(END, f"Student {i}: \n", 'header')
        outputtext.insert(END, studentview(student) + "\n")
    averagepercentage = totalpercentage / len(students) if students else 0
    #Shows the summary of total students and class average
    outputtext.insert(END, "~" * 77 + "\n", 'separator')
    outputtext.insert(END, "📋 Class Summary\n", 'title')
    outputtext.insert(END, f"Total Students: {len(students)}\n", 'summary')
    outputtext.insert(END, f"Class Average Percentage: {averagepercentage:.1f}%\n", 'summary')
    outputtext.config(state=DISABLED)

def viewindividualstudent():
    """To view details of an individual student by selecting from a different window."""
    clearoutput()
    selectionwindow = Toplevel(main)
    selectionwindow.title("Select a Student")
    selectionwindow.geometry("500x500")
    selectionwindow.iconphoto(False, ImageTk.PhotoImage(file=r"Exercise 3\images\selectionwindowlogo.png"))
    selectionwindow.resizable(0, 0)
    selectionwindow.configure(bg=COLORS['headerbg'])
    
    #Designing header frame for selection window
    headerframe = Frame(selectionwindow, bg=COLORS['brightpurple'], height=60)
    headerframe.pack(fill=X, side=TOP)
    headerframe.pack_propagate(False)
    Label(headerframe, text="Select a Student", font=("Courier New", 16, "bold"),
          bg=COLORS['brightpurple'], fg=COLORS['textcolor']).pack(expand=True)
    
    #Designing content frame for listbox
    contentframe = Frame(selectionwindow, bg=COLORS['headerbg'])
    contentframe.pack(fill=BOTH, expand=True, padx=20, pady=20)

    #Designing listbox with purple theme
    listbox = Listbox(contentframe, width=55, height=15, font=("Courier New", 11),
                      bg=COLORS['listboxbg'], fg=COLORS['listboxfg'],
                      selectbackground=COLORS['mediumpurple'],
                      selectforeground=COLORS['textcolor'],
                      relief=RAISED, bd=2)
    listbox.pack(pady=15, fill=BOTH, expand=True)

    #Adding students to the listbox
    for student in students:
        listbox.insert(END, f"{student['code']} - {student['name']}")

    #Designing button frame
    buttonframe = Frame(contentframe, bg=COLORS['headerbg'])
    buttonframe.pack(fill=X, pady=10)
    
    def studentdisplay():
        """To Display the selected student's details in the output area."""
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            selectedstudent = students[index]
            outputtext.config(state=NORMAL)
            outputtext.delete(1.0, END)
            outputtext.insert(END, "🎓 Individual Student Record\n", 'title')
            outputtext.insert(END, studentview(selectedstudent))
            outputtext.config(state=DISABLED)
            selectionwindow.destroy()
        else:
            messagebox.showwarning("Warning", "Please select a student!")
    #Designing buttons to view student
    Button(buttonframe, text="👤 View Selected Student", command=studentdisplay,
           bg=COLORS['buttonbg'], fg=COLORS['buttonfg'],
           font=("Courier New", 11, "bold"), relief=RAISED, bd=3, padx=15, pady=8,
           activebackground=COLORS['violet'], activeforeground=COLORS['textcolor']).pack(side=LEFT, padx=10)
    #Designing cancel button
    Button(buttonframe, text="❌ Cancel", command=selectionwindow.destroy,
           bg=COLORS['mediumpurple'], fg=COLORS['textcolor'],
           font=("Courier New", 11), relief=RAISED, bd=2, padx=15, pady=8,
           activebackground=COLORS['lightpurple']).pack(side=RIGHT, padx=10)

def highestscore():
    clearoutput()
    """To show the student with the highest total score."""
    outputtext.config(state=NORMAL)
    outputtext.delete(1.0, END)
    higheststudent = None
    highestpercentage = -1
    #To find the highest scoring student
    for student in students:
        _, percentage, _ = resultcalculation(student)
        if percentage > highestpercentage:
            highestpercentage = percentage
            higheststudent = student
    #To display the highest scoring student's details
    if higheststudent:
        outputtext.insert(END, "🏆 Student with Highest Total Score:\n", 'title')
        outputtext.insert(END, studentview(higheststudent))
    outputtext.config(state=DISABLED)

def lowestscore():
    clearoutput()
    """To show the student with the lowest total score."""
    outputtext.config(state=NORMAL)
    outputtext.delete(1.0, END)
    loweststudent = None
    lowestpercentage = 101
    #To find the lowest scoring student
    for student in students:
        _, percentage, _ = resultcalculation(student)
        if percentage < lowestpercentage:
            lowestpercentage = percentage
            loweststudent = student
    #To display the lowest scoring student's details
    if loweststudent:
        outputtext.insert(END, "📉 Student with Lowest Total Score:\n", 'title')
        outputtext.insert(END, studentview(loweststudent))
    outputtext.config(state=DISABLED)

#Designing header frame of the main window
headerframe = Frame(main, bg=COLORS['headerbg'], height=80)
headerframe.pack(fill=X, side=TOP)
headerframe.pack_propagate(False)

#Designing title label and adding it to header frame
titlelabel = Label(headerframe, text="🎓 Student Manager", 
                   font=("Courier New", 20, "bold"), 
                   bg=COLORS['headerbg'], 
                   fg=COLORS['textcolor'])
titlelabel.pack(expand=True)

#Creating menu bar and designing it with purple theme
menubar = Menu(main, bg=COLORS['mediumpurple'], fg=COLORS['textcolor'],
               activebackground=COLORS['violet'], activeforeground=COLORS['textcolor'],
               relief=RAISED, bd=2)
main.config(menu=menubar)

#Creating Options menu
optionsmenu = Menu(menubar, tearoff=0, bg=COLORS['lightpurple'], fg=COLORS['listboxfg'],
                   activebackground=COLORS['violet'], activeforeground=COLORS['textcolor'],
                   font=("Courier New", 10))

#Adding commands to the Options menu
menubar.add_cascade(label="📊 Options", menu=optionsmenu)
optionsmenu.add_command(label="👥 View All Students", command=studentsviewall)
optionsmenu.add_command(label="👤 View Individual Student", command=viewindividualstudent)
optionsmenu.add_command(label="🏆 Show Highest Scoring Student", command=highestscore)
optionsmenu.add_command(label="📉 Show Lowest Scoring Student", command=lowestscore)
optionsmenu.add_separator()
optionsmenu.add_command(label="🚪 Exit", command=main.quit)

#Creating main content frame with purple styling
maincontent = Frame(main, bg=COLORS['darkpurple'])
maincontent.pack(fill=BOTH, expand=True, padx=15, pady=15)

#designing the output frame to show results 
outputframe = LabelFrame(maincontent, text="📈 Student Records", padx=15, pady=15,
                         bg=COLORS['mediumdarkpurple'], fg=COLORS['textcolor'],
                         font=("Courier New", 14, "bold"), relief=RAISED, bd=3,
                         labelanchor='n')
outputframe.pack(fill=BOTH, expand=True)

#Designing inner frame 
innerframe = Frame(outputframe, bg=COLORS['lavender'], relief=SUNKEN, bd=2)
innerframe.pack(fill=BOTH, expand=True, padx=5, pady=5)

#scrollbar for the text area with design
scrollbar = Scrollbar(innerframe, bg=COLORS['mediumpurple'], 
                      troughcolor=COLORS['lightpurple'],
                      elementborderwidth=2)
scrollbar.pack(side=RIGHT, fill=Y)

#Designing output text area with pruple colors
outputtext = Text(innerframe, font=("Courier New", 11), yscrollcommand=scrollbar.set,
                  bg=COLORS['lavender'], fg=COLORS['listboxfg'],
                  selectbackground=COLORS['mediumpurple'], 
                  selectforeground=COLORS['textcolor'],
                  state=DISABLED, wrap=WORD, padx=15, pady=15,
                  relief=FLAT)
outputtext.pack(fill=BOTH, expand=True)

#Tag configurations for different text styles
outputtext.tag_configure('title', foreground=COLORS['brightpurple'], 
                         font=("Courier New", 13, "bold"),
                         justify='center')
outputtext.tag_configure('header', foreground=COLORS['headerbg'], 
                         font=("Courier New", 11, "bold"))
outputtext.tag_configure('separator', foreground=COLORS['mediumpurple'],
                         font=("Courier New", 10))
outputtext.tag_configure('summary', foreground=COLORS['darkpurple'], 
                         font=("Courier New", 11, "bold"))

#Connecting scrollbar to the text area
scrollbar.config(command=outputtext.yview)

#To show welcome message in the output area
outputtext.config(state=NORMAL)
outputtext.insert(END, "✨ Welcome to Student Manager! ✨\n\n", 'title')
outputtext.insert(END, "> This is to view the Student Records\n")
outputtext.insert(END, "> To view more, Click on Options", 'header')
outputtext.config(state=DISABLED) #To make the text area read-only

loadstudentdata()
main.mainloop()