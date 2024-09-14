from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

# Add Task Function
def add_task():
    task_string = task_field.get().strip()
    if not task_string:
        messagebox.showwarning('Input Error', 'Please enter a task.')
    else:
        tasks.append(task_string)
        the_cursor.execute('INSERT INTO tasks (title) VALUES (?)', (task_string,))
        update_task_list()
        task_field.delete(0, END)

# Update Listbox
def update_task_list():
    clear_listbox()
    for task in tasks:
        task_listbox.insert(END, task)

# Delete Selected Task
def delete_task():
    selected_task = task_listbox.curselection()
    if not selected_task:
        messagebox.showwarning('Selection Error', 'Please select a task to delete.')
    else:
        task_to_delete = task_listbox.get(selected_task)
        tasks.remove(task_to_delete)
        the_cursor.execute('DELETE FROM tasks WHERE title = ?', (task_to_delete,))
        update_task_list()

# Delete All Tasks
def delete_all_tasks():
    if messagebox.askyesno('Confirm Deletion', 'Are you sure you want to delete all tasks?'):
        tasks.clear()
        the_cursor.execute('DELETE FROM tasks')
        update_task_list()

# Clear Listbox
def clear_listbox():
    task_listbox.delete(0, END)

# Close Application
def close_app():
    the_connection.commit()
    the_cursor.close()
    guiWindow.destroy()

# Retrieve Tasks from Database
def retrieve_tasks():
    tasks.clear()
    for row in the_cursor.execute('SELECT title FROM tasks'):
        tasks.append(row[0])

if __name__ == "__main__":
    # GUI Setup
    guiWindow = Tk()
    guiWindow.title("Task Manager")
    guiWindow.geometry("600x400")
    guiWindow.configure(bg="#E8F6EF")

    # SQLite Setup
    the_connection = sql.connect('tasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT)')

    tasks = []

    # Frames for Better Layout Management
    top_frame = Frame(guiWindow, bg="#E8F6EF", pady=10)
    top_frame.pack(fill="x")

    middle_frame = Frame(guiWindow, bg="#E8F6EF", pady=10)
    middle_frame.pack(fill="x")

    bottom_frame = Frame(guiWindow, bg="#E8F6EF", pady=10)
    bottom_frame.pack(fill="x")

    # Widgets in the Top Frame
    task_label = Label(top_frame, text="Enter Task:", font=("Arial", 12), bg="#E8F6EF")
    task_label.pack(side=LEFT, padx=10)

    task_field = Entry(top_frame, font=("Arial", 12), width=40)
    task_field.pack(side=LEFT, padx=10)

    add_button = Button(top_frame, text="Add Task", font=("Arial", 12), bg="#58D68D", command=add_task)
    add_button.pack(side=LEFT, padx=10)

    # Listbox in the Middle Frame
    task_listbox = Listbox(middle_frame, font=("Arial", 12), selectmode=SINGLE, width=55, height=10, bg="#FEF9E7")
    task_listbox.pack(padx=10, pady=10)

    # Buttons in the Bottom Frame
    del_button = Button(bottom_frame, text="Delete Task", font=("Arial", 12), bg="#E74C3C", command=delete_task)
    del_button.pack(side=LEFT, padx=20)

    del_all_button = Button(bottom_frame, text="Delete All", font=("Arial", 12), bg="#E74C3C", command=delete_all_tasks)
    del_all_button.pack(side=LEFT, padx=20)

    exit_button = Button(bottom_frame, text="Exit", font=("Arial", 12), bg="#AAB7B8", command=close_app)
    exit_button.pack(side=LEFT, padx=20)

    # Retrieve tasks from database
    retrieve_tasks()
    update_task_list()

    guiWindow.mainloop()
