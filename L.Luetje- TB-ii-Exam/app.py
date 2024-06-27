import tkinter as tk
from tkinter import messagebox
import pandas as pd
from src.helpers import clear_widgets, add_image
import os
from datetime import datetime, timedelta
import random


todo_lists = {}
screen_width = 800  #width
screen_height = 600  #height


root = tk.Tk()

# Initialize Tkinter variables
user_id = tk.StringVar()
name = tk.StringVar()
username = tk.StringVar()
use_multiple_people = tk.BooleanVar()
people_names = []
todo_entry = None
week_frame1 = None
week_frame2 = None

images = []

def save_todo_items(user_id):
    """Save todo items for a user to a CSV file."""
    todo_data = []
    for date, items in todo_lists.items():
        for item in items:
            todo_data.append({"user_id": user_id, "date": date, "todo_item": item})
    todo_df = pd.DataFrame(todo_data)
    todo_df.to_csv("data/todo_data.csv", index=False, mode='a', header=not os.path.isfile("data/todo_data.csv"))

def load_todo_items(user_id):
    """Load todo items for a user from a CSV file."""
    global todo_lists
    todo_lists = {}
    try:
        todo_data = pd.read_csv("data/todo_data.csv", dtype={'user_id': str})
        user_todo_data = todo_data[todo_data["user_id"] == user_id]
        for _, row in user_todo_data.iterrows():
            date = row["date"]
            todo_item = row["todo_item"]
            if date not in todo_lists:
                todo_lists[date] = []
            todo_lists[date].append(todo_item)
    except FileNotFoundError:
        pass

def create_homepage_button(root):
    #Homebutton
    homepage_button = tk.Button(root, text="🏠", command=lambda: create_homepage(root), font=("Arial", 14), relief="flat", bd=0)
    homepage_button.pack(side=tk.BOTTOM)

def user_check(root):
    #Check if user ID is empty or already used + proceed to the todo page if valid
    user_id_value = user_id.get().strip()
    if not user_id_value:
        tk.messagebox.showwarning("Oooopss...", "User ID cannot be empty.")
        return

    try:
        user_data = pd.read_csv("data/users_data.csv", dtype={'user_id': str})
        user_ids = list(user_data["user_id"].astype(str))
    except FileNotFoundError:
        tk.messagebox.showwarning("Oooooppss...", "Have you registered your user ID? Please try again 🙂")
        return

    if user_id_value in user_ids:
        clear_widgets(root)
        create_todo_page(root, user_id_value)
    else:
        tk.messagebox.showwarning("Oooooppss...", "Have you registered your user ID? Please try again 🙂")

def create_return_userpage(root):
   #Login fpr returning users
    clear_widgets(root)
    images.append(add_image(root, "images/postit.jpeg", screen_width, screen_height))

    tk.Label(root, text="Enter your user ID", fg="black", font=("Arial", 16)).place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    tk.Entry(root, textvariable=user_id, fg="black", font=("Arial", 14)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    tk.Button(root, text="Login", font=("Arial", 14), command=lambda: user_check(root), relief="flat", bd=0).place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    create_homepage_button(root)

def enter_user_data(root):
    #Register a new user
    username_value = username.get().strip()
    if not username_value:
        tk.messagebox.showwarning("Oooppss..", "Your User ID is empty.")
        return

    try:
        user_data = pd.read_csv("data/users_data.csv", dtype={'user_id': str})
        user_ids = list(user_data["user_id"].astype(str))
    except FileNotFoundError:
        user_ids = []

    if username_value in user_ids:
        tk.messagebox.showwarning("Ooopppss...", "Your Username already exists, please choose another")
    else:
        new_user_data = pd.DataFrame([{"name_of_user": name.get(), "user_id": username_value}])
        new_user_data.to_csv("data/users_data.csv", index=False, mode='a', header=not os.path.isfile("data/users_data.csv"))
        clear_widgets(root)
        create_todo_page(root, username_value)

def create_new_userpage(root):
    #REgistration page fpr new users
    clear_widgets(root)
    images.append(add_image(root, "images/postit.jpeg", screen_width, screen_height))

    tk.Label(root, text="What's your name? :)", fg="black", font=("Arial", 16)).place(relx=0.5, rely=0.25, anchor=tk.CENTER)
    tk.Entry(root, textvariable=name, fg="black", font=("Arial", 14)).place(relx=0.5, rely=0.35, anchor=tk.CENTER)
    tk.Label(root, text="Enter your user ID", fg="black", font=("Arial", 16)).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    tk.Entry(root, textvariable=username, fg="black", font=("Arial", 14)).place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    tk.Button(root, text="Register", font=("Arial", 14), command=lambda: enter_user_data(root), relief="flat", bd=0).place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    create_homepage_button(root)

def add_todo_items(root, user_id_value):
    #Adding ToDo items to the users list
    todo_text = todo_entry.get()
    use_multiple_people_value = use_multiple_people.get()
    people_names_list = people_names if use_multiple_people_value else ["Person 1"]

    if not people_names_list or (use_multiple_people_value and len(people_names_list) == 1):
        tk.messagebox.showwarning("WARNING", "Please enter names for multiple people.")
        return

    todo_items = [item.strip() for item in todo_text.replace(',', '.').split('.') if item.strip()]
    random.shuffle(todo_items)
    if todo_items:
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        start_of_next_week = end_of_week + timedelta(days=1)

        assigned_tasks_week1 = {name.strip(): [] for name in people_names_list}
        assigned_tasks_week2 = {name.strip(): [] for name in people_names_list}

        for i, todo_item in enumerate(todo_items):
            person_week1 = people_names_list[i % len(people_names_list)].strip()
            person_week2 = people_names_list[(i + 1) % len(people_names_list)].strip()

            date_week1 = (start_of_week + timedelta(days=i % 7)).strftime("%Y-%m-%d")
            date_week2 = (start_of_next_week + timedelta(days=i % 7)).strftime("%Y-%m-%d")

            assigned_tasks_week1[person_week1].append((date_week1, todo_item))
            assigned_tasks_week2[person_week2].append((date_week2, todo_item))

        for person, tasks in assigned_tasks_week1.items():
            for date, task in tasks:
                if date not in todo_lists:
                    todo_lists[date] = []
                todo_lists[date].append(f"{person}: {task}")

        for person, tasks in assigned_tasks_week2.items():
            for date, task in tasks:
                if date not in todo_lists:
                    todo_lists[date] = []
                todo_lists[date].append(f"{person}: {task}")

        messagebox.showinfo("🎉YEAH🎉", "YOUR TO DO LIST IS READY! GOOD LUCK")
        todo_entry.delete(0, tk.END)
        save_todo_items(user_id_value)
        display_todo_items(root)

def display_todo_items(root):
    #Two calenders/plan for two weeks
    for widget in week_frame1.winfo_children():
        widget.destroy()
    for widget in week_frame2.winfo_children():
        widget.destroy()

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_next_week = start_of_week + timedelta(days=7)

    for i in range(7):
        day = start_of_week + timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        frame = tk.Frame(week_frame1, borderwidth=1, relief="solid", bg="lightblue")
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(frame, text=days_of_week[i], font="Arial 14 bold", bg="lightblue").pack()
        listbox = tk.Listbox(frame, bg="#6599FF", font=("Arial", 12))
        listbox.pack(fill=tk.BOTH, expand=True)

        if date_str in todo_lists:
            for item in todo_lists[date_str]:
                listbox.insert(tk.END, item)

    #2nd week
    for i in range(7):
        day = start_of_next_week + timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        frame = tk.Frame(week_frame2, borderwidth=1, relief="solid", bg="lightblue")
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(frame, text=days_of_week[i], font="Arial 14 bold", bg="lightblue", fg="black").pack()
        listbox = tk.Listbox(frame, bg="#F76D6D", fg="black", font=("Arial", 12))
        listbox.pack(fill=tk.BOTH, expand=True)

        if date_str in todo_lists:
            for item in todo_lists[date_str]:
                listbox.insert(tk.END, item)

def create_todo_page(root, user_id_value):
    #Creating the todo page
    global todo_entry, week_frame1, week_frame2
    clear_widgets(root)
    load_todo_items(user_id_value)

    tk.Label(root, text="📝What do you need to do?(Please separate your ToDo's by a comma or period)📝", font=("Arial", 16)).pack()
    todo_entry = tk.Entry(root, width=80, font=("Arial", 14))
    todo_entry.pack()

    tk.Label(root, text="👤Is someone helping?👤", font=("Arial", 16)).pack()
    tk.Checkbutton(root, variable=use_multiple_people, font=("Arial", 14), command=toggle_people_entry).pack()
    tk.Button(root, text="✅Generate To Do List ✅", font=("Arial", 18), command=lambda: add_todo_items(root, user_id_value), relief="flat", bd=0).pack(pady=10)

    week_frame1 = tk.Frame(root)
    week_frame1.pack(fill=tk.BOTH, expand=True)

    week_frame2 = tk.Frame(root)
    week_frame2.pack(fill=tk.BOTH, expand=True)

    display_todo_items(root)
    create_homepage_button(root)

def toggle_people_entry():
   #option to add two people
    if use_multiple_people.get():
        create_people_entry_window()
    else:
        global people_names
        people_names = []

def create_people_entry_window():
   #window for multiple people
    global people_window, people_entry
    people_window = tk.Toplevel(root)
    people_window.title("🧍")
    people_window.geometry("700x200")

    tk.Label(people_window, text="Please enter names (separated by comma):", font=("Arial", 14)).pack(pady=10)
    people_entry = tk.Entry(people_window, width=30, font=("Arial", 14))
    people_entry.pack(pady=10)
    tk.Button(people_window, text="Submit", font=("Arial", 14), command=submit_people_names, relief="flat", bd=0).pack(pady=10)

def submit_people_names():
    #box to enter the other names
    global people_names
    names = people_entry.get().split(',')
    people_names = [name.strip() for name in names if name.strip()]
    people_window.destroy()

def show_info():
    #showing info of EVENTually
    messagebox.showinfo("Application Benefits", "EVENTually helps you manage your tasks efficiently. You can create and assign tasks and view them by week - without stressful discussions. Made for flatshares, friends and organised Queens")

def create_homepage(root):
    #homepage: new +returning users
    clear_widgets(root)
    images.append(add_image(root, "images/postit.jpeg", screen_width, screen_height))

    tk.Label(root, text="EVENTually", font="Arial 24 bold", fg="black", bg="white").place(x=280, y=20)
    button_padding = 70

    tk.Button(root, text="I'm new", font=("Arial", 18, "bold"), command=lambda: create_new_userpage(root), relief="flat", bd=0).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    tk.Button(root, text="Login", font=("Arial", 18, "bold"), command=lambda: create_return_userpage(root), relief="flat", bd=0).place(relx=0.5, rely=0.4 + button_padding / 400, anchor=tk.CENTER)
    tk.Button(root, text="ℹ️", font=("Arial", 18, "bold"), command=show_info, relief="flat", bd=0).place(relx=0.5, rely=0.4 + 2 * (button_padding / 400), anchor=tk.CENTER)

create_homepage(root)
root.mainloop()
