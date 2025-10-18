# Exercise 3 : Student Manager 

import tkinter as tk
from tkinter import ttk, messagebox
import os

root = tk.Tk()
root.title("Student Manager")
root.geometry("600x400")
root.resizable(0, 0)

title = tk.Label(root, text = 'Student Manager', font = ('Helvetica', 15, 'bold'))
title.place(relx = 0.5, rely = 0.1, anchor = 'center')

# Viewing Individual Student Record
tk.Label(root, text = 'View Individual Student Record:', font = ('Helvetica', 10)).place(x = 80, y = 150)

# Information of the Students
def load_students(filename = "studentMarks.txt"):
    students_dict = {}
    filepath = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) == 6:
                    name, number, coursework, exam, overall, grade = parts
                    students_dict[name] = (number, int(coursework), int(exam), int(overall), grade)
                else:
                    print(f"⚠️ Skipped invalid line: {line}")
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
    return students_dict

students = load_students()
selected_student = tk.StringVar()
names = list(students.keys())
entry = ttk.Combobox(root, textvariable = selected_student, values = names, width = 22, state = 'readonly')
entry.place(x=270, y=150)

# Box that show's the information of the students
info_frame = tk.Frame(root, bg = 'lightgrey', bd = 2, relief = 'groove')
info_frame.place(x = 80, y = 200, width = 440, height = 150)

# Save student records to file
def save_to_file():
    with open("studentMarks.txt", "w", encoding = "utf-8") as f:
        for name, (number, coursework, exam, overall, grade) in students.items():
            f.write(f"{name},{number},{coursework},{exam},{overall},{grade}\n")

# Capitalization of first letter when changing or adding a new name in the records
def capitalize_name(name):
    return name.title()

# Find student despite Case-Insensitive by name
def find_student(target):
    target = target.strip().lower()
    for name, data in students.items():
        if name.lower() == target or data[0].lower() == target:
            return name
    return None

# Automatically check if new record is highest or lowest
def check_highest_lowest(new_name):
    highest = max(students.items(), key = lambda x: x[1][3])
    lowest = min(students.items(), key = lambda x: x[1][3])
    overall = students[new_name][3]
    if overall == highest[1][3]:
        messagebox.showinfo("New Highest Score!", f"{new_name} now has the highest overall score ({overall}). 🎉")
    elif overall == lowest[1][3]:
        messagebox.showinfo("New Lowest Score!", f"{new_name} now has the lowest overall score ({overall}). 😢")

# Show all students in a scrollable text area inside info_frame
def show_all():
    for w in info_frame.winfo_children():
        w.destroy()
    txt = tk.Text(info_frame, bg = 'lightgrey', bd = 0, wrap = 'word', font = ('Helvetica', 9))
    txt.pack(fill = 'both', expand=True, padx = 6, pady = 6)
    for name, (number, coursework, exam, overall, grade) in students.items():
        txt.insert('end', f"  Name: {name}\n")
        txt.insert('end', f"  Number: {number}\n")
        txt.insert('end', f"  Coursework: {coursework}\n")
        txt.insert('end', f"  Exam: {exam}\n")
        txt.insert('end', f"  Overall: {overall}\n")
        txt.insert('end', f"  Grade: {grade}\n\n")
    txt.config(state='disabled')

# Highest Score Function
def show_highest():
    for w in info_frame.winfo_children():
        w.destroy()
    txt = tk.Text(info_frame, bg = 'lightgrey', bd = 0, wrap = 'word', font = ('Helvetica', 9))
    txt.pack(fill = 'both', expand = True, padx = 6, pady = 6)
    name, data = max(students.items(), key = lambda x: x[1][3])
    number, coursework, exam, overall, grade = data
    txt.insert('end', f"  Name: {name}\n")
    txt.insert('end', f"  Number: {number}\n")
    txt.insert('end', f"  Coursework: {coursework}\n")
    txt.insert('end', f"  Exam: {exam}\n")
    txt.insert('end', f"  Overall: {overall}\n")
    txt.insert('end', f"  Grade: {grade}\n\n")
    txt.config(state='disabled')

# Lowest Score Function
def show_lowest():
    for w in info_frame.winfo_children():
        w.destroy()
    txt = tk.Text(info_frame, bg = 'lightgrey', bd = 0, wrap = 'word', font = ('Helvetica', 9))
    txt.pack(fill = 'both', expand = True, padx = 6, pady = 6)
    name, data = min(students.items(), key=lambda x: x[1][3])
    number, coursework, exam, overall, grade = data
    txt.insert('end', f"  Name: {name}\n")
    txt.insert('end', f"  Number: {number}\n")
    txt.insert('end', f"  Coursework: {coursework}\n")
    txt.insert('end', f"  Exam: {exam}\n")
    txt.insert('end', f"  Overall: {overall}\n")
    txt.insert('end', f"  Grade: {grade}\n\n")
    txt.config(state='disabled')

# Individual Student Record Button Function
def view_record():
    name = selected_student.get()
    if not name:
        messagebox.showinfo("No selection", "Please select a student.")
        return
    for w in info_frame.winfo_children():
        w.destroy()
    txt = tk.Text(info_frame, bg = 'lightgrey', bd = 0, wrap = 'word', font = ('Helvetica', 9))
    txt.pack(fill = 'both', expand = True, padx = 6, pady = 6)
    number, coursework, exam, overall, grade = students[name]
    txt.insert('end', f"  Name: {name}\n")
    txt.insert('end', f"  Number: {number}\n")
    txt.insert('end', f"  Coursework: {coursework}\n")
    txt.insert('end', f"  Exam: {exam}\n")
    txt.insert('end', f"  Overall: {overall}\n")
    txt.insert('end', f"  Grade: {grade}\n\n")
    txt.config(state='disabled')

# Sorting of Records based on User Preferences
def sort_records():
    sort_win = tk.Toplevel(root)
    sort_win.title("Sort Records")
    sort_win.geometry("250x150")

    tk.Label(sort_win, text = "Choose sorting order:").pack(pady = 10)

    def sort_ascending():
        global students
        students = dict(sorted(students.items(), key = lambda x: x[1][3]))
        entry['values'] = list(students.keys())
        show_all()
        save_to_file()
        messagebox.showinfo("Sorted", "Student records sorted in ascending order by Overall.")
        sort_win.destroy()

    def sort_descending():
        global students
        students = dict(sorted(students.items(), key = lambda x: x[1][3], reverse = True))
        entry['values'] = list(students.keys())
        show_all()
        save_to_file()
        messagebox.showinfo("Sorted", "Student records sorted in descending order by Overall.")
        sort_win.destroy()

    tk.Button(sort_win, text="Ascending", font=('Helvetica', 10), command=sort_ascending).pack(pady=5, fill='x', padx=20)
    tk.Button(sort_win, text="Descending", font=('Helvetica', 10), command=sort_descending).pack(pady=5, fill='x', padx=20)

# Adding a Student Record Function
def add_record():
    add_win = tk.Toplevel(root)
    add_win.title("Add Student Record")
    add_win.geometry("300x350")

    fields = ["Name", "Number", "Coursework", "Exam", "Overall", "Grade"]
    entries = {}

    for i, field in enumerate(fields):
        tk.Label(add_win, text = field).grid(row = i, column = 0, padx = 5, pady = 5)
        e = tk.Entry(add_win)
        e.grid(row = i, column = 1, padx = 5, pady = 5)
        entries[field] = e

    def save_new():
        try:
            name = capitalize_name(entries["Name"].get())
            number = entries["Number"].get().strip()
            coursework = int(entries["Coursework"].get())
            exam = int(entries["Exam"].get())
            overall = int(entries["Overall"].get())
            grade = entries["Grade"].get().strip().upper()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for Coursework, Exam, Overall.")
            return
        students[name] = (number, coursework, exam, overall, grade)
        save_to_file()
        check_highest_lowest(name)
        entry['values'] = list(students.keys())
        show_all()
        add_win.destroy()

    tk.Button(add_win, text="Save", font=('Helvetica',10), command=save_new).grid(row=len(fields), column=0, columnspan=2, pady=10)

# Deleting a Student Record Function
def delete_record():
    del_win = tk.Toplevel(root)
    del_win.title("Delete Student Record")
    del_win.geometry("300x150")

    tk.Label(del_win, text="Enter Name or Student Code:").pack(pady = 5)
    target_entry = tk.Entry(del_win)
    target_entry.pack()

    def delete():
        name = find_student(target_entry.get())
        if name:
            del students[name]
            save_to_file()
            entry['values'] = list(students.keys())
            show_all()
            del_win.destroy()
        else:
            messagebox.showerror("Not Found", "Student not found.")

    tk.Button(del_win, text = "Delete", font = ('Helvetica',10), command = delete).pack(pady = 10)

# Updating a Student Record Function
def update_record():
    upd_win = tk.Toplevel(root)
    upd_win.title("Update Student Record")
    upd_win.geometry("300x150")

    tk.Label(upd_win, text="Enter Name or Student Code:").pack(pady = 5)
    target_entry = tk.Entry(upd_win)
    target_entry.pack()

    def find():
        name = find_student(target_entry.get())
        if not name:
            messagebox.showerror("Not Found", "Student not found.")
            return

        edit_win = tk.Toplevel(upd_win)
        edit_win.title(f"Update Record - {name}")
        edit_win.geometry("300x300")

        fields = ["Number", "Coursework", "Exam", "Overall", "Grade"]
        entries = {}
        current = students[name]

        for i, field in enumerate(fields):
            tk.Label(edit_win, text = field).grid(row = i, column = 0, padx = 5, pady = 5)
            e = tk.Entry(edit_win)
            e.grid(row = i, column = 1, padx = 5, pady = 5)
            e.insert(0, current[i])
            entries[field] = e

        def save():
            try:
                number = entries["Number"].get().strip()
                coursework = int(entries["Coursework"].get())
                exam = int(entries["Exam"].get())
                overall = int(entries["Overall"].get())
                grade = entries["Grade"].get().strip().upper()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers.")
                return
            students[name] = (number, coursework, exam, overall, grade)
            save_to_file()
            check_highest_lowest(name)
            entry['values'] = list(students.keys())
            show_all()
            edit_win.destroy()
            upd_win.destroy()

        tk.Button(edit_win, text="Save Changes", font=('Helvetica',10), command=save).grid(row=len(fields), column=0, columnspan=2, pady=10)

    tk.Button(upd_win, text="Find", font=('Helvetica',10), command=find).pack(pady=10)

# Pop-Up Menu Button Function
def open_menu():
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label = "Sort Records", command = sort_records)
    menu.add_command(label = "Add Record", command = add_record)
    menu.add_command(label = "Delete Record", command = delete_record)
    menu.add_command(label = "Update Record", command = update_record)
    menu.tk_popup(root.winfo_pointerx(), root.winfo_pointery())

# Functions of the Buttons
root.grid_rowconfigure(0, minsize = 40)

btn_opts = {'height': 2, 'bd': 2, 'relief': 'groove'}
button_frame = tk.Frame(root)
button_frame.place(relx = 0.5, rely = 0.18, anchor = 'n')  

tk.Button(button_frame, text = 'View All Student Records', **btn_opts, font = ('Helvetica', 10), command = show_all).grid(row = 0, column = 0, sticky = 'EW', padx = 5)
tk.Button(button_frame, text = 'Show Highest Score', **btn_opts, font = ('Helvetica', 10), command = show_highest).grid(row = 0, column = 1, sticky = 'EW', padx = 5)
tk.Button(button_frame, text = 'Show Lowest Score', **btn_opts, font = ('Helvetica', 10), command = show_lowest).grid(row = 0, column = 2, sticky = 'EW', padx = 5)
tk.Button(button_frame, text = '...', **btn_opts, font = ('Helvetica', 10), command = open_menu).grid(row = 0, column = 3, sticky = 'EW', padx = 5)

tk.Button(root, text = 'View Record', **btn_opts, font = ('Helvetica', 10), command = view_record).place(x = 433, y = 138)

# Run
root.mainloop()