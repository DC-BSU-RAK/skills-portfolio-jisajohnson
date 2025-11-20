from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import random
import os

#To create the main window
main = Tk()
main.title("Alexa, Tell me a joke")
main.geometry("1200x675")
main.iconphoto(False, ImageTk.PhotoImage(file=r"Exercise 2\images\alexalogoicon.png"))
main.resizable(0,0)

#Global variables for current joke and punchline label
currentjoke = None
punchlinelabel = None

def clearscreen():
    """This is used to clear the widgets from the screen while changing the background"""
    for clear in main.winfo_children():
        clear.destroy()

def startscreen():
    clearscreen()
    """This is for the start screen with the start button"""
    # Image for the introduction and how to be placed
    IntroImage = ImageTk.PhotoImage(Image.open(r"Exercise 2\images\alexa.jpg"))
    IntroImageLabel = Label(main, image=IntroImage)
    IntroImageLabel.image = IntroImage
    IntroImageLabel.place(x=0, y=0, relwidth=1, relheight=1)
    # Start button to start the quiz
    startbutton = Button(main, text="Alexa, Tell me a Joke", font=("Courier New", 16, "bold"), bg="#5fcbf4", fg="white", width=30, height=2, command=jokescreen)
    startbutton.place(relx=0.5, rely=0.80, anchor=CENTER)

def jokesfilesetup():
    """Load jokes from the randomJokes.txt file"""
    jokes = []
    #Another way to open files using os module to create file paths
    file_path = os.path.join("Exercise 2", "randomJokes.txt")
    #This is in case the file is not found or there is an error reading it
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                if line and "?" in line:
                    parts = line.split("?", 1)
                    setup = parts[0] + "?"
                    punchline = parts[1] if len(parts) > 1 else ""
                    jokes.append((setup, punchline))
    except FileNotFoundError:
        messagebox.showerror("Error", "Jokes file not found!")
    return jokes

def jokescreen():
    """Display a random joke setup"""
    clearscreen()
    BackgroundImage = ImageTk.PhotoImage(Image.open(r"Exercise 2\images\alexa.jpg"))
    BackgroundImageLabel = Label(main, image=BackgroundImage)
    BackgroundImageLabel.image = BackgroundImage
    BackgroundImageLabel.place(x=0, y=0, relwidth=1, relheight=1)

    #Load jokes from file
    jokes = jokesfilesetup()
    global currentjoke, punchlinelabel
    currentjoke = random.choice(jokes)

    #Content frame to hold the joke and buttons
    contentframe = Frame(main, bg="white", bd=2, relief="raised")
    contentframe.place(relx=0.5, rely=0.5, anchor=CENTER, width=800, height=400)

    #Frame to show the joke setup and punchline
    jokeframe = Frame(contentframe, bg="black", bd=0)
    jokeframe.pack(pady=20, padx=20, fill=BOTH, expand=True)

    #Setup label for the joke
    setuplabel = Label(jokeframe, text=currentjoke[0], font=("Courier New", 16, "bold"), bg="black", fg="white", wraplength=700, justify="center")
    setuplabel.pack(pady=20, padx=20, fill=BOTH, expand=True)

    #Punchline label
    punchlinelabel = Label(jokeframe, text="", font=("Courier New", 14, "italic"), bg="black", fg="#CCCCCC", wraplength=700, justify="center")
    punchlinelabel.pack(pady=10, padx=20, fill=BOTH, expand=True)
    
    #Button frame for punchline, next joke, and quit buttons
    buttonframe = Frame(contentframe, bg="white")
    buttonframe.pack(pady=20)
    
    #Shows the punchline of the joke
    punchlinebutton = Button(buttonframe, text="Show Punchline", font=("Courier New", 14, "bold"), bg="#5fcbf4", fg="white", width=15, height=1, command=showpunchline)
    punchlinebutton.grid(row=0, column=0, padx=10)
    
    #Next Joke button to load another joke
    nextjokebutton = Button(buttonframe, text="Next Joke", font=("Courier New", 14, "bold"), bg="#5fcbf4", fg="white", width=15, height=1, command=jokescreen)
    nextjokebutton.grid(row=0, column=1, padx=10)
    
    #Quit button to exit the program
    quitbutton = Button(buttonframe, text="Quit", font=("Courier New", 14, "bold"), bg="#fd3636", fg="white", width=15, height=1, command=quitprogram)
    quitbutton.grid(row=0, column=2, padx=10)

def showpunchline():
    """Display the punchline of the current joke"""
    global currentjoke, punchlinelabel
    if currentjoke and punchlinelabel:
        punchlinelabel.config(text=currentjoke[1])

def quitprogram():
    """To exit the program with confirmation"""
    if messagebox.askyesno("Exit?", "Are you sure you want to exit?"):
        main.destroy()

startscreen()
main.mainloop()