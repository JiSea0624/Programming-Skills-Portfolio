# Exercise 2 : Alexa tell me a Joke 

import tkinter as tk
import random, os

root = tk.Tk()
root.title("Alexa Tell Me A Joke")
root.geometry("600x600")
root.resizable(0, 0)

# Frame setup
frame = tk.Frame(root, bg = "lightgreen", width = 550, height = 550)
frame.pack_propagate(False)
frame.pack(expand=True)

# List of Jokes in txt file
def load_jokes(filename = "randomJokes.txt"):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(filepath, "r", encoding = "utf-8") as f:
            return {q.strip(): a.strip() for q, a in 
                    (line.strip().split("=", 1) for line in f if "=" in line)}
    except FileNotFoundError:
        return {"File not found!": "Make sure randomJokes.txt is in the same folder."}

# Load jokes
jokes = load_jokes()

# Function to clear frame
def clear_frame():
    for w in frame.winfo_children(): w.destroy()

# Function to create labels easily
def make_label(text, size, y, bold = False, color = "black"):
    style = ("Helvetica", size, "bold") if bold else ("Helvetica", size)
    tk.Label(frame, text = text, font = style, fg = color, bg = "lightgreen",
             wraplength = 500, justify = "center").place(relx = 0.5, rely = y, anchor = "center")

# Function to show a joke
def joke():
    clear_frame()
    q, a = random.choice(list(jokes.items()))
    make_label(f"Alexa: {q}", 18, 0.35)
    ans = tk.Label(frame, text = "", font = ("Helvetica", 25, "bold"), fg = "green", bg = "lightgreen", wraplength = 500, justify = "center")
    ans.place(relx = 0.5, rely = 0.5, anchor = "center")

    # Punchline Button
    tk.Button(frame, text = "Show Answer", font = ("Helvetica", 16, "bold"), bg = "green", fg = "white", command = lambda: ans.config(text = a)).place(relx = 0.5, rely = 0.65, anchor = "center")
    
    # Another Joke Button
    tk.Button(frame, text = "Tell me another Joke", font = ("Helvetica", 16, "bold"), bg = "green", fg = "white", command = joke).place(relx = 0.5, rely = 0.75, anchor = "center")

# Function to check user input
def check_input(event=None):
    if entry.get().strip().lower() == "tell me a joke":
        joke()
    else:
        response_label.config(text = "Alexa: I didn’t catch that! Try typing 'tell me a joke'.")
    entry.delete(0, tk.END)

# Show menu : Welcome Message & Instruction of the Site
def show_menu():
    clear_frame()
    make_label("Welcome to Alexa's Joke Site!", 22, 0.3, bold = True)
    make_label("Type 'tell me a joke' below and press Enter to hear a joke!", 14, 0.45)

    global entry, response_label
    entry = tk.Entry(frame, font = ("Helvetica", 16), width = 30, justify = "center")
    entry.place(relx = 0.5, rely = 0.55, anchor = "center")
    entry.bind("<Return>", check_input)

    response_label = tk.Label(frame, text = "", font = ("Helvetica", 14, "italic"), bg = "lightgreen", fg = "darkgreen")
    response_label.place(relx = 0.5, rely = 0.65, anchor = "center")

# Run
show_menu()
root.mainloop()