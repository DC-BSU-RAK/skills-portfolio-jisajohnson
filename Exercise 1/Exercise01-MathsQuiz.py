from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import random

#To start the application 
main = Tk()
main.title("Maths Quiz")
main.geometry("1200x675")
main.iconphoto(False, ImageTk.PhotoImage(file=r"Exercise 1\images\mathssymbol.png"))
main.resizable(0,0)

#Global variables for the Maths Quiz
score = 0 #Current Score
currentquestion = 0 #Current question no.
totalquestions = 10 #Total no. of questions
attempts = 0 #Total Attempts for a question is 2
currentproblem = None #Current Problem
currentanswer = None #Correct Answer for the current problem
difficulty = None #Current difficulty level
operation = None #The present operation for the current problem

def clearscreen():
    """This is used to clear the widgets from the screen while changing the background"""
    for clear in main.winfo_children():
        clear.destroy()

def introscreen():
    clearscreen()
    """This is for the start screen with the start button"""
    #Image for the introduction and how to be placed
    IntroImage = ImageTk.PhotoImage(Image.open(r"Exercise 1\images\MathsQuizfront.jpg"))
    IntroImageLabel = Label(main, image=IntroImage)
    IntroImageLabel.image = IntroImage
    IntroImageLabel.place(x=0, y=0, relwidth=1, relheight=1)
    #Start button to start the quiz
    startbutton = Button(main, text="START", font=("Comic Sans MS", 16, "bold"), command=displayMenu, bg="#ec407a", fg="white", width=20, height=2)
    startbutton.place(relx=0.5, rely=0.75, anchor=CENTER)

def displayMenu():
    clearscreen()
    """This screen is to show the levels present in this quiz"""
    #Background image setting for level screen
    levelscreenimage = ImageTk.PhotoImage(Image.open(r"Exercise 1\images\MathsQuizbg.jpg"))
    levelscreenLabel = Label(main, image=levelscreenimage)
    levelscreenLabel.image = levelscreenimage
    levelscreenLabel.place(x=0, y=0, relwidth=1, relheight=1)
    #Shows the title
    heading = Label(main, text="LEVELS", font=("Comic Sans MS", 25, "bold"), fg="#000000", bg="#ffffff")
    heading.place(relx=0.5, rely=0.25, anchor=CENTER)
    """Level buttons and given designated colours and fonts to match the theme"""
    #Easy button
    easybutton = Button(main, text="EASY", font=("Comic Sans MS", 16), width=20, height=2, bg="#43a047", command=lambda: startquiz("EASY"))
    easybutton.place(relx=0.5, rely=0.4, anchor=CENTER)
    #moderate button    
    moderatebutton = Button(main, text="MODERATE", font=("Comic Sans MS", 16), width=20, height=2, bg="#f5bd1b", command=lambda: startquiz("MODERATE"))  # Fixed to "MODERATE"
    moderatebutton.place(relx=0.5, rely=0.55, anchor=CENTER)
    #advanced button
    advancedbutton = Button(main, text="ADVANCED", font=("Comic Sans MS", 16), width=20, height=2, bg="#d81a60", fg="white", command=lambda: startquiz("ADVANCED"))
    advancedbutton.place(relx=0.5, rely=0.7, anchor=CENTER)

def startquiz(level):
    """To start the quiz after clicking on the level the user wants"""
    global difficulty, score, currentquestion, attempts
    difficulty = level
    score = 0
    currentquestion = 1
    attempts = 0
    quizDisplay()

def randomInt():
    """This is to give random numbers to the users so that when they retry the quiz they could get different numbers"""
    if difficulty == "EASY":
        return random.randint(1, 9) 
    elif difficulty == "MODERATE": 
        return random.randint(10, 99)
    elif difficulty == "ADVANCED":
        return random.randint(1000, 9999)
     
def decideOperation():
    """This is to ensure that the operation are only addition or substraction"""
    return random.choice(['+', '-'])

def displayProblem():
    """To display the problem on the quiz screen and how the score and progress is shown"""
    global currentproblem, currentanswer, operation
    number1 = randomInt()
    number2 = randomInt()
    operation = decideOperation()
    #To avoid negative numbers in subtraction
    if operation == '-' and number1 < number2:
        number1, number2 = number2, number1
    #to set the current problem
    currentproblem = (number1, number2, operation)
    #To calculate the current answer
    if operation == '+':
        currentanswer = number1 + number2
    else:
        currentanswer = number1 - number2
    #To Display the problem    
    problemtext = f"{number1} {operation} {number2} = ____"
    problemlabel.config(text=problemtext)
    #To clear the entry box and focus on it
    answerentry.delete(0, END)
    answerentry.focus()
    #To show the progress and score
    progresslabel.config(text=f"Question: {currentquestion}/{totalquestions}")
    scorelabel.config(text=f"Score: {score}")

def isCorrect(useranswer):
    """To ensure if the user's answer is correct or not"""
    return useranswer == currentanswer

def checkanswer():
    """To confirm the user's answer is right and to give points accordingly"""
    global score, attempts, currentquestion
    try:
        useranswer = int(answerentry.get())
        attempts += 1

        if isCorrect(useranswer):
            """If the answer is correct, marks will be given based on attempts"""
            if attempts == 1:
                score += 10
                messagebox.showinfo("Correct Answer!", "Amazing! 10 points")
            else: 
                score += 5
                messagebox.showinfo("Correct!", "Good job! 5 points")

            currentquestion += 1
            attempts = 0
            #To ensure if the quiz is over or not
            if currentquestion > totalquestions:
                resultsscreen()
            else:
                displayProblem()
        #To check if the answer is incorrect or if the user has entered something other than a number        
        else:
            if attempts == 1:
                messagebox.showerror("Incorrect!", "Wrong Answer, Try again!")
                answerentry.delete(0, END)
                answerentry.focus()
            else:
                messagebox.showerror("Incorrect!", f"The correct answer was {currentanswer}")  
                currentquestion += 1
                attempts = 0
                if currentquestion > totalquestions:  
                    resultsscreen()
                else:
                    displayProblem()
    except ValueError:
        messagebox.showerror("Invalid!", "Please enter a valid number.")
        answerentry.delete(0, END)
        answerentry.focus()

def displayResults():
    """To calculate the percentage and grade based on the score"""
    percentage = (score / 100) * 100
    #Depending on the percentage the grade is given
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:  
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"                     

def resultsscreen():
    clearscreen()
    """"This screen shows the final results once the quiz is completed"""
    #Setting the background image for results screen
    resultsscreenimage = ImageTk.PhotoImage(Image.open(r"Exercise 1\images\MathsQuizbg.jpg"))
    resultsscreenLabel = Label(main, image=resultsscreenimage)
    resultsscreenLabel.image = resultsscreenimage
    resultsscreenLabel.place(x=0, y=0, relwidth=1, relheight=1)

    grade = displayResults()
    #To display the results
    resultsdisplay = Frame(main, bg="white")
    resultsdisplay.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=300)
    resultslabel = Label(resultsdisplay, text="RESULTS", font=("Comic Sans MS", 20, "bold"), bg="white")  
    resultslabel.pack(pady=20)
    #To show the final score 
    finalscorelabel = Label(resultsdisplay, text=f"Final Score: {score}/100", font=("Comic Sans MS", 16), bg="white")  
    finalscorelabel.pack(pady=10)
    #To show the grade achieved
    gradelabel = Label(resultsdisplay, text=f"Grade: {grade}", font=("Comic Sans MS", 18, "bold"), bg="white")  
    gradelabel.pack(pady=10)
    #The button frame for play again and exit buttons
    buttonframe = Frame(resultsdisplay, bg="white")
    buttonframe.pack(pady=20)
    #play again button design and function
    playagainbutton = Button(buttonframe, text="Play Again", font=("Comic Sans MS", 14), command=displayMenu, bg="#43a047", fg="white", width=12)  
    playagainbutton.pack(side=LEFT, padx=10)
    #exit button design and function
    exitbutton = Button(buttonframe, text="Exit", font=("Comic Sans MS", 14), command=main.quit, bg="#d81a60", fg="white", width=12)
    exitbutton.pack(side=LEFT, padx=10)

def quizDisplay():
    clearscreen()
    """This is to show the quiz screen where the problems are displayed"""
    quizscreenimage = ImageTk.PhotoImage(Image.open(r"Exercise 1\images\MathsQuizbg.jpg"))
    quizscreenLabel = Label(main, image=quizscreenimage)
    quizscreenLabel.image = quizscreenimage
    quizscreenLabel.place(x=0, y=0, relwidth=1, relheight=1)

    global problemlabel, answerentry, scorelabel, progresslabel
    #The design of the quiz frame 
    quizframe = Frame(main, bg="white")
    quizframe.place(relx=0.5, rely=0.5, anchor=CENTER, width=600, height=400)  
    
    #The design of the difficulty label
    difficultylabel = Label(quizframe, text=f"Level: {difficulty}", font=("Comic Sans MS", 18, "bold"), bg="white")  
    difficultylabel.pack(pady=15)
    
    #The design of the progress label
    progresslabel = Label(quizframe, text=f"Question: {currentquestion}/{totalquestions}", 
                         font=("Comic Sans MS", 14), bg="white")
    progresslabel.pack(pady=8)
    
    #The design of the problem label
    problemlabel = Label(quizframe, text="", font=("Comic Sans MS", 24, "bold"), bg="white") 
    problemlabel.pack(pady=20)
    
    #The design of the answer frame
    answerframe = Frame(quizframe, bg="white")
    answerframe.pack(pady=15)
    
    #The design of the answer label 
    answerlabel = Label(answerframe, text="Answer:", font=("Comic Sans MS", 16), bg="white") 
    answerlabel.pack(side=LEFT, padx=8)
    
    #The design of the answer entry box 
    answerentry = Entry(answerframe, font=("Comic Sans MS", 16), width=12, justify=CENTER) 
    answerentry.pack(side=LEFT, padx=8)
    answerentry.bind('<Return>', lambda event: checkanswer())
    
    #The design of the submit button 
    submitbutton = Button(quizframe, text="Submit", font=("Comic Sans MS", 16), 
                         command=checkanswer, bg="#43a047", fg="white", width=15, height=1) 
    submitbutton.pack(pady=15)
    
    #The design of the results info frame
    resultsinfoframe = Frame(quizframe, bg="white")
    resultsinfoframe.pack(pady=15)
    
    #The design of the score label 
    scorelabel = Label(resultsinfoframe, text=f"Score: {score}", font=("Comic Sans MS", 14), bg="white") 
    scorelabel.pack(side=LEFT, padx=25)
    
    #To display the problem
    displayProblem()

#To run the application
introscreen()
main.mainloop()