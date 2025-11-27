from tkinter import *
from PIL import ImageTk
from tkinter import messagebox, simpledialog
import os

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

def sortstudents():
    clearoutput()
    def performsort(sortby, order):
        """To sort the students based on the selected order"""
        if sortby == "name":
            students.sort(key=lambda x: x['name'].lower(), reverse=(order == "desc")) #Sorting by name
        elif sortby == "code":
            students.sort(key=lambda x: x['code'], reverse=(order == "desc")) #Sorting by student code
        studentsviewall()
        sortwindow.destroy()

    #Create sorting window
    sortwindow = Toplevel(main)
    sortwindow.title("Sort Students")
    sortwindow.geometry("400x350")
    sortwindow.configure(bg=COLORS['headerbg'])
    sortwindow.iconphoto(False, ImageTk.PhotoImage(file=r"Exercise 3\images\selectionwindowlogo.png"))
    sortwindow.resizable(0, 0)
    
    #Designing header frame for sort window
    headerframe = Frame(sortwindow, bg=COLORS['brightpurple'], height=60)
    headerframe.pack(fill=X, side=TOP)
    headerframe.pack_propagate(False)
    Label(headerframe, text="Sort Students", font=("Courier New", 16, "bold"),
          bg=COLORS['brightpurple'], fg=COLORS['textcolor']).pack(expand=True)
    
    #Designing content frame
    contentframe = Frame(sortwindow, bg=COLORS['headerbg'], padx=20, pady=20)
    contentframe.pack(fill=BOTH, expand=True)
    
    #Label and radio buttons for sort window
    Label(contentframe, text="Sort by:", font=("Courier New", 12, "bold"),
          bg=COLORS['headerbg'], fg=COLORS['textcolor']).pack(anchor=W, pady=(0, 10))
    
    sortvar = StringVar(value="name")
    Radiobutton(contentframe, text="Name", variable=sortvar, value="name",
                bg=COLORS['headerbg'], fg=COLORS['textcolor'], 
                selectcolor=COLORS['mediumpurple'], font=("Courier New", 11)).pack(anchor=W)
    Radiobutton(contentframe, text="Student Code", variable=sortvar, value="code",
                bg=COLORS['headerbg'], fg=COLORS['textcolor'],
                selectcolor=COLORS['mediumpurple'], font=("Courier New", 11)).pack(anchor=W)
    
    #Choice for ascending or descending order
    Label(contentframe, text="Order:", font=("Courier New", 12, "bold"),
          bg=COLORS['headerbg'], fg=COLORS['textcolor']).pack(anchor=W, pady=(20, 10))
    
    ordervar = StringVar(value="asc")
    Radiobutton(contentframe, text="Ascending (A-Z, 0-9)", variable=ordervar, value="asc",
                bg=COLORS['headerbg'], fg=COLORS['textcolor'],
                selectcolor=COLORS['mediumpurple'], font=("Courier New", 11)).pack(anchor=W)
    Radiobutton(contentframe, text="Descending (Z-A, 9-0)", variable=ordervar, value="desc",
                bg=COLORS['headerbg'], fg=COLORS['textcolor'],
                selectcolor=COLORS['mediumpurple'], font=("Courier New", 11)).pack(anchor=W)
    
    #Designing the button frame
    buttonframe = Frame(contentframe, bg=COLORS['headerbg'])
    buttonframe.pack(fill=X, pady=(20, 0))

    #Designing sort and cancel buttons
    Button(buttonframe, text="✅ Sort", 
           command=lambda: performsort(sortvar.get(), ordervar.get()),
           bg=COLORS['buttonbg'], fg=COLORS['buttonfg'],
           font=("Courier New", 11, "bold"), relief=RAISED, bd=3, padx=15, pady=8).pack(side=LEFT, padx=5)
    
    Button(buttonframe, text="❌ Cancel", command=sortwindow.destroy,
           bg=COLORS['mediumpurple'], fg=COLORS['textcolor'],
           font=("Courier New", 11), relief=RAISED, bd=2, padx=15, pady=8).pack(side=RIGHT, padx=5)

def savestudentdata():
    """This function saves the student data back to the text file."""
    try:
        with open("Exercise 3/studentMarks.txt", "w") as f:
            f.write(f"{len(students)}\n")
            for student in students:
                f.write(f"{student['code']},{student['name']},{student['cw1']},{student['cw2']},{student['cw3']},{student['exam']}\n")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Error saving student data: {str(e)}") #If the code doesn't work, it shows an error message
        return False
    
def addstudent():
    """To add a new student record."""
    
    def savenewstudent():
        """To save the new student record in the txt file."""
        try:
            #To get data from the user input fields
            code = int(codeentry.get())
            name = nameentry.get().strip()
            cw1 = int(cw1entry.get())
            cw2 = int(cw2entry.get())
            cw3 = int(cw3entry.get())
            exam = int(examentry.get())
            
            #The maximum marks allowed for coursework and exam
            if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20 and 0 <= exam <= 100):
                messagebox.showerror("Error", "Marks must be: CW1-3 (0-20), Exam (0-100)")
                return
            
            #To ensure student code is unique and to prevent duplicates
            if any(student['code'] == code for student in students):
                messagebox.showerror("Error", "Student code already exists!")
                return
            
            #Creating new student record
            newstudent = {
                "code": code,
                "name": name,
                "cw1": cw1,
                "cw2": cw2,
                "cw3": cw3,
                "exam": exam
            }
            
            students.append(newstudent) 
            
            #To save the new student data to the file
            if savestudentdata():
                messagebox.showinfo("Success", "Student added successfully!")
                addwindow.destroy()
                studentsviewall()  #Shows the old records along with the new one
            else:
                students.pop()  #Remove the student if saving failed
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for all fields!") #In case the user didn't add details properly
    
    # Create add student window
    addwindow = Toplevel(main)
    addwindow.title("Add New Student")
    addwindow.geometry("500x450")
    addwindow.configure(bg=COLORS['headerbg'])
    addwindow.iconphoto(False, ImageTk.PhotoImage(file=r"Exercise 3\images\selectionwindowlogo.png"))
    addwindow.resizable(0, 0)
    
    #Designing header frame for add student window
    headerframe = Frame(addwindow, bg=COLORS['brightpurple'], height=60)
    headerframe.pack(fill=X, side=TOP)
    headerframe.pack_propagate(False)
    Label(headerframe, text="Add New Student", font=("Courier New", 16, "bold"),
          bg=COLORS['brightpurple'], fg=COLORS['textcolor']).pack(expand=True)
    
    #Designing content frame
    contentframe = Frame(addwindow, bg=COLORS['headerbg'], padx=20, pady=20)
    contentframe.pack(fill=BOTH, expand=True)
    
    #Form fields for student details
    fields = [
        ("Student Code:", "codeentry"),
        ("Full Name:", "nameentry"),
        ("Coursework 1 (0-20):", "cw1entry"),
        ("Coursework 2 (0-20):", "cw2entry"),
        ("Coursework 3 (0-20):", "cw3entry"),
        ("Exam Mark (0-100):", "examentry")
    ]
    
    entries = {} #To store the entry details
    for i, (labeltext, entryname) in enumerate(fields):
        Label(contentframe, text=labeltext, font=("Courier New", 11),
              bg=COLORS['headerbg'], fg=COLORS['textcolor']).grid(row=i, column=0, sticky=W, pady=10)
        #entry fields for user input
        entry = Entry(contentframe, font=("Courier New", 11), width=20)
        entry.grid(row=i, column=1, padx=10, pady=10)
        entries[entryname] = entry
    
    #Getting references to the entry fields
    codeentry = entries['codeentry']
    nameentry = entries['nameentry']
    cw1entry = entries['cw1entry']
    cw2entry = entries['cw2entry']
    cw3entry = entries['cw3entry']
    examentry = entries['examentry']
    
    #Designing button frame and the buttons
    buttonframe = Frame(contentframe, bg=COLORS['headerbg'])
    buttonframe.grid(row=len(fields), column=0, columnspan=2, pady=20)

    #Designing save button
    Button(buttonframe, text="💾 Save Student", command=savenewstudent,
           bg=COLORS['buttonbg'], fg=COLORS['buttonfg'],
           font=("Courier New", 11, "bold"), relief=RAISED, bd=3, padx=15, pady=8).pack(side=LEFT, padx=10)
    
    #Designing cancel button
    Button(buttonframe, text="❌ Cancel", command=addwindow.destroy,
           bg=COLORS['mediumpurple'], fg=COLORS['textcolor'],
           font=("Courier New", 11), relief=RAISED, bd=2, padx=15, pady=8).pack(side=RIGHT, padx=10)

def deletestudent():
    clearoutput()    
    def performdelete():
        """To delete the selected student record."""
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            student = students[index]
            #Confirmation screen before deleting
            confirm = messagebox.askyesno("Confirm Delete", 
                                         f"Are you sure you want to delete {student['name']} (Code: {student['code']})?")
            if confirm:
                students.pop(index)
                if savestudentdata():
                    messagebox.showinfo("Success", "Student deleted successfully!") #Shows success message
                    deletewindow.destroy()
                    studentsviewall()  #Shows the remaining records after deletion
                else:
                    messagebox.showerror("Error", "Failed to save changes!") #In case it doesn't save, it shows an error
        else:
            messagebox.showwarning("Warning", "Please select a student to delete!") #In case no student is selected
    
    #Creating delete student window
    deletewindow = Toplevel(main)
    deletewindow.title("Delete Student")
    deletewindow.geometry("500x500")
    deletewindow.configure(bg=COLORS['headerbg'])
    deletewindow.iconphoto(False, ImageTk.PhotoImage(file=r"Exercise 3\images\selectionwindowlogo.png"))
    deletewindow.resizable(0, 0)
    
    #Designing header frame for delete student window
    headerframe = Frame(deletewindow, bg=COLORS['brightpurple'], height=60)
    headerframe.pack(fill=X, side=TOP)
    headerframe.pack_propagate(False)
    Label(headerframe, text="Delete Student", font=("Courier New", 16, "bold"),
          bg=COLORS['brightpurple'], fg=COLORS['textcolor']).pack(expand=True)
    
    #Designing content frame
    contentframe = Frame(deletewindow, bg=COLORS['headerbg'], padx=20, pady=20)
    contentframe.pack(fill=BOTH, expand=True)
    
    Label(contentframe, text="Select a student to delete:", font=("Courier New", 12, "bold"),
          bg=COLORS['headerbg'], fg=COLORS['textcolor']).pack(anchor=W, pady=(0, 10))
    
    #Designing the listbox to show students
    listbox = Listbox(contentframe, width=55, height=15, font=("Courier New", 11),
                      bg=COLORS['listboxbg'], fg=COLORS['listboxfg'],
                      selectbackground=COLORS['mediumpurple'],
                      selectforeground=COLORS['textcolor'],
                      relief=RAISED, bd=2)
    listbox.pack(pady=10, fill=BOTH, expand=True)
    
    #It shows how the students are displayed in the listbox
    for student in students:
        listbox.insert(END, f"{student['code']} - {student['name']}")
    
    #Designing button frame
    buttonframe = Frame(contentframe, bg=COLORS['headerbg'])
    buttonframe.pack(fill=X, pady=10)
    
    #Designing the delete button
    Button(buttonframe, text="🗑️ Delete", command=performdelete,
           bg='#FF6B6B', fg=COLORS['textcolor'],
           font=("Courier New", 11, "bold"), relief=RAISED, bd=3, padx=15, pady=8).pack(side=LEFT, padx=10)
    
    #Designing the cancel button
    Button(buttonframe, text="❌ Cancel", command=deletewindow.destroy,
           bg=COLORS['mediumpurple'], fg=COLORS['textcolor'],
           font=("Courier New", 11), relief=RAISED, bd=2, padx=15, pady=8).pack(side=RIGHT, padx=10)

def updatestudent():
    """To update an existing student record."""
    clearoutput()
    def performupdate():
        """To update the selected student record."""
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            selectedstudent = students[index]
            updatewindow.destroy()
            showsubupdatemenu(selectedstudent, index)
        else:
            messagebox.showwarning("Warning", "Please select a student to update!")

    #Create update student window 
    updatewindow = Toplevel(main)
    updatewindow.title("Select Student to Update")
    updatewindow.geometry("500x500")
    updatewindow.configure(bg=COLORS['headerbg'])
    updatewindow.iconphoto(False, ImageTk.PhotoImage(file=r"Exercise 3\images\selectionwindowlogo.png"))
    updatewindow.resizable(0, 0)
    
    #Designing header frame for update student window
    headerframe = Frame(updatewindow, bg=COLORS['brightpurple'], height=60)
    headerframe.pack(fill=X, side=TOP)
    headerframe.pack_propagate(False)
    Label(headerframe, text="Select Student to Update", font=("Courier New", 16, "bold"),
          bg=COLORS['brightpurple'], fg=COLORS['textcolor']).pack(expand=True)
    
    #Designing content frame
    contentframe = Frame(updatewindow, bg=COLORS['headerbg'], padx=20, pady=20)
    contentframe.pack(fill=BOTH, expand=True)
    
    Label(contentframe, text="Select a student to update:", font=("Courier New", 12, "bold"),
          bg=COLORS['headerbg'], fg=COLORS['textcolor']).pack(anchor=W, pady=(0, 10))
    
    #Designing the listbox to show students
    listbox = Listbox(contentframe, width=55, height=15, font=("Courier New", 11),
                      bg=COLORS['listboxbg'], fg=COLORS['listboxfg'],
                      selectbackground=COLORS['mediumpurple'],
                      selectforeground=COLORS['textcolor'],
                      relief=RAISED, bd=2)
    listbox.pack(pady=10, fill=BOTH, expand=True)
    
    #Displaying students in the listbox
    for student in students:
        listbox.insert(END, f"{student['code']} - {student['name']}")
    
    #Designing button frame
    buttonframe = Frame(contentframe, bg=COLORS['headerbg'])
    buttonframe.pack(fill=X, pady=10)
    
    #Designing the update button
    Button(buttonframe, text="✏️ Update", command=performupdate,
           bg=COLORS['buttonbg'], fg=COLORS['buttonfg'],
           font=("Courier New", 11, "bold"), relief=RAISED, bd=3, padx=15, pady=8).pack(side=LEFT, padx=10)
    
    #Designing the cancel button
    Button(buttonframe, text="❌ Cancel", command=updatewindow.destroy,
           bg=COLORS['mediumpurple'], fg=COLORS['textcolor'],
           font=("Courier New", 11), relief=RAISED, bd=2, padx=15, pady=8).pack(side=RIGHT, padx=10)

def showsubupdatemenu(student, index):
    """Show the update menu for a specific student."""
    
    def updatefield(fieldname, currentvalue, validation_func=None):
        """Updating a specific field of the student record."""
        newvalue = simpledialog.askstring(f"Update {fieldname}", 
                                         f"Current {fieldname}: {currentvalue}\nEnter new {fieldname}:",
                                         parent=subupdatewindow)
        #For user input validation and updating the record
        if newvalue is not None:
            if newvalue.strip():
                try:
                    # Validate and convert if needed
                    if validation_func:
                        validatedvalue = validation_func(newvalue)
                    else:
                        validatedvalue = newvalue.strip()
                    
                    #To Update the student record
                    student[fieldname] = validatedvalue
                    
                    #To save the updated student data to the file
                    if savestudentdata():
                        messagebox.showinfo("Success", f"{fieldname.capitalize()} updated successfully!")
                        subupdatewindow.destroy()
                        studentsviewall()
                    else:
                        messagebox.showerror("Error", "Failed to save changes!")
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showwarning("Warning", f"{fieldname.capitalize()} cannot be empty!")
    
    #Validating student name to be not empty
    def validatename(name):
        name = name.strip()
        if not name:
            raise ValueError("Name cannot be empty!")
        return name
    #Validating student code to be unique and numeric
    def validatecode(code):
        try:
            code = int(code)
            #To avoid duplicate student codes
            if any(s['code'] == code and s != student for s in students):
                raise ValueError("Student code already exists!")
            return code
        except ValueError:
            raise ValueError("Student code must be a number!")
    #Validating marks to be within the allowed range
    def validatemark(mark, maxmark, fieldname):
        try:
            mark = int(mark)
            if not (0 <= mark <= maxmark):
                raise ValueError(f"{fieldname} must be between 0 and {maxmark}!")
            return mark
        except ValueError:
            raise ValueError(f"{fieldname} must be a number between 0 and {maxmark}!")
    
    #Creating submenu window for updating student details
    subupdatewindow = Toplevel(main)
    subupdatewindow.title(f"Update {student['name']}")
    subupdatewindow.geometry("500x700")
    subupdatewindow.configure(bg=COLORS['headerbg'])
    subupdatewindow.iconphoto(False, ImageTk.PhotoImage(file=r"Exercise 3\images\selectionwindowlogo.png"))
    subupdatewindow.resizable(0, 0)
    
    #Designing header frame for update submenu window
    headerframe = Frame(subupdatewindow, bg=COLORS['brightpurple'], height=60)
    headerframe.pack(fill=X, side=TOP)
    headerframe.pack_propagate(False)
    Label(headerframe, text=f"Update {student['name']}", font=("Courier New", 16, "bold"),
          bg=COLORS['brightpurple'], fg=COLORS['textcolor']).pack(expand=True)
    
    #Designing content frame
    contentframe = Frame(subupdatewindow, bg=COLORS['headerbg'], padx=20, pady=20)
    contentframe.pack(fill=BOTH, expand=True)
    
    #To display current student information
    infoframe = Frame(contentframe, bg=COLORS['lightpurple'], relief=RAISED, bd=2, padx=10, pady=10)
    infoframe.pack(fill=X, pady=(0, 20))
    
    Label(infoframe, text="Current Information:", font=("Courier New", 12, "bold"),
          bg=COLORS['lightpurple'], fg=COLORS['darkpurple']).pack(anchor=W)
    
    #Displaying student details
    infotext = (f"Student Code: {student['code']}\n"
                 f"Name: {student['name']}\n"
                 f"Corsework 1: {student['cw1']}\n"
                 f"Coursework 2: {student['cw2']}\n"
                 f"Coursework 3: {student['cw3']}\n"
                 f"Exam: {student['exam']}")
    
    Label(infoframe, text=infotext, font=("Courier New", 10),
          bg=COLORS['lightpurple'], fg=COLORS['listboxfg']).pack(anchor=W, pady=(5, 0))
    
    #To select which field to update
    Label(contentframe, text="Select field to update:", font=("Courier New", 12, "bold"),
          bg=COLORS['headerbg'], fg=COLORS['textcolor']).pack(anchor=W, pady=(0, 15))
    
    #Creating buttons for each field
    fields = [
        ("👤 Student Name", "name", lambda: updatefield("name", student["name"], validatename)),
        ("🔢 Student Code", "code", lambda: updatefield("code", student["code"], validatecode)),
        ("📊 Coursework 1", "cw1", lambda: updatefield("cw1", student["cw1"], 
                                                     lambda x: validatemark(x, 20, "Coursework 1"))),
        ("📊 Coursework 2", "cw2", lambda: updatefield("cw2", student["cw2"], 
                                                     lambda x: validatemark(x, 20, "Coursework 2"))),
        ("📊 Coursework 3", "cw3", lambda: updatefield("cw3", student["cw3"], 
                                                     lambda x: validatemark(x, 20, "Coursework 3"))),
        ("📝 Exam Mark", "exam", lambda: updatefield("exam", student["exam"], 
                                                   lambda x: validatemark(x, 100, "Exam")))
    ]
    
    #Creating buttons for each field to update
    for i, (button_text, field_name, command) in enumerate(fields):
        Button(contentframe, text=button_text, command=command,
               bg=COLORS['mediumpurple'], fg=COLORS['textcolor'],
               font=("Courier New", 11), relief=RAISED, bd=2, 
               width=20, pady=8).pack(pady=5)
    
    #Designing cancel button
    Button(contentframe, text="❌ Cancel", command=subupdatewindow.destroy,
           bg=COLORS['mediumpurple'], fg=COLORS['textcolor'],
           font=("Courier New", 11), relief=RAISED, bd=2, padx=15, pady=8).pack(pady=15)
    
def exitmanager():
    """To exit the Student Manager application."""
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        main.quit()
        main.destroy()    

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

#Creating and designing View menu
viewmenu = Menu(menubar, tearoff=0, bg=COLORS['lightpurple'], fg=COLORS['listboxfg'],
                   activebackground=COLORS['violet'], activeforeground=COLORS['textcolor'],
                   font=("Courier New", 10))

#Creating and designing Edit menu
editmenu = Menu(menubar, tearoff=0, bg=COLORS['lightpurple'], fg=COLORS['listboxfg'],
                   activebackground=COLORS['violet'], activeforeground=COLORS['textcolor'],
                   font=("Courier New", 10))

#Adding commands to the View menu
menubar.add_cascade(label="📊 View", menu=viewmenu)
viewmenu.add_command(label="👥 View All Students", command=studentsviewall)
viewmenu.add_command(label="👤 View Individual Student", command=viewindividualstudent)
viewmenu.add_command(label="🏆 Show Highest Scoring Student", command=highestscore)
viewmenu.add_command(label="📉 Show Lowest Scoring Student", command=lowestscore)
viewmenu.add_command(label="📊 Sort Student Records", command=sortstudents)

#Adding commands to the Edit menu
menubar.add_cascade(label="✏️ Edit", menu=editmenu)
editmenu.add_command(label="➕ Add Student Record", command=addstudent)
editmenu.add_command(label="🗑️ Delete Student Record", command=deletestudent)
editmenu.add_command(label="✏️ Update Student Record", command=updatestudent)

#Adding Exit command directly to menubar
menubar.add_command(label="🚪 Exit", command=exitmanager)

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
outputtext.insert(END, "> This is to view and edit the Student Records\n")
outputtext.insert(END, "> To view the data, Click on View\n", 'header')
outputtext.insert(END, "> To edit the data, Click on Edit", 'header')
outputtext.config(state=DISABLED) #To make the text area read-only

loadstudentdata()
main.mainloop()