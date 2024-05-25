from tkinter import *
import random
import sqlite3

root = Tk()
root.title('workouts')
root.geometry('600x500')

#create a database or connect to one
conn = sqlite3.connect('workout_log.db')

#create a cursor
c = conn.cursor()

# create table
# c.execute("""CREATE TABLE workouts (
#         date text,
#         exercise text,
#         weight text,
#         set_num integer,
#         reps integer
#         )""")

#create delete function
def delete():
    #create a database or connect to one
    conn = sqlite3.connect('workout_log.db')
    #create a cursor
    c = conn.cursor()

    #delete a record
    c.execute("DELETE from workouts WHERE oid= " + delete_box.get())

    #commit changes to database
    conn.commit()
    #close connection
    conn.close()


def update():
    #create a database or connect to one
    conn = sqlite3.connect('workout_log.db')
    #create a cursor
    c = conn.cursor()

    record_id = delete_box.get()
    c.execute("""UPDATE workouts SET
        date = :date,
        exercise = :exercise,
        weight = :weight,
        set_num = :set_num,
        reps = :reps
              
        WHERE oid = :oid""",
        {
        'date': date_editor.get(),
        'exercise': exercise_editor.get(),
        'weight': weight_editor.get(),
        'set_num': set_num_editor.get(),
        'reps': reps_editor.get(),
        'oid': record_id
        })

    #commit changes to database
    conn.commit()
    #close connection
    conn.close()
    editor.destroy()


#create edit function
def edit():
    global editor
    editor = Tk()
    editor.title('Update a record')
    editor.geometry('600x500')

    #create a database or connect to one
    conn = sqlite3.connect('workout_log.db')
    #create a cursor
    c = conn.cursor()

    record_id = delete_box.get()
    #query the database
    c.execute("SELECT * FROM workouts WHERE oid = " + record_id)
    records = c.fetchall()

    #create Global variables for text box names
    global date_editor
    global exercise_editor
    global weight_editor
    global set_num_editor
    global reps_editor

    #create text boxes
    date_editor = Entry(editor, width = 30)
    date_editor.grid(row = 0, column = 1, padx = 20, pady = (10,0))
    exercise_editor = Entry(editor, width = 30)
    exercise_editor.grid(row = 1, column = 1)
    weight_editor = Entry(editor, width = 30)
    weight_editor.grid(row = 2, column = 1)
    set_num_editor = Entry(editor, width = 30)
    set_num_editor.grid(row = 3, column = 1)
    reps_editor = Entry(editor, width = 30)
    reps_editor.grid(row = 4, column = 1)

    #create text box labels
    date_editor_label = Label(editor, text= 'Date')
    date_editor_label.grid(row = 0, column = 0, pady = (10,0))
    exercise_editor_label = Label(editor, text= 'Exercise name')
    exercise_editor_label.grid(row = 1, column = 0)
    weight_editor_label = Label(editor, text='Weight (lbs)')
    weight_editor_label.grid(row = 2, column = 0)
    set_num_editor_label = Label(editor, text= 'Set number')
    set_num_editor_label.grid(row = 3, column = 0)
    reps_editor_label = Label(editor, text='Number of reps')
    reps_editor_label.grid(row = 4, column = 0)

    #loop through results
    for record in records:
        date_editor.insert(0, record[0])
        exercise_editor.insert(0, record[1])
        weight_editor.insert(0, record[2])
        set_num_editor.insert(0, record[3])
        reps_editor.insert(0, record[4])

    #create a save button
    edit_button = Button(editor, text='Save record', command= update)
    edit_button.grid(row = 5, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 145)


#create submit function for database
def submit():
    #create a database or connect to one
    conn = sqlite3.connect('workout_log.db')
    #create a cursor
    c = conn.cursor()

    #insert into table
    c.execute("INSERT INTO workouts VALUES (:date, :exercise, :weight, :set_num, :reps)",
            {
                'date': date.get(),
                'exercise': exercise.get(),
                'weight': weight.get(),
                'set_num': set_num.get(),
                'reps': reps.get()
            })

    #commit changes to database
    conn.commit()

    #close connection
    conn.close()

    #clear the text boxes
    date.delete(0, END)
    exercise.delete(0, END)
    weight.delete(0, END)
    set_num.delete(0, END)
    reps.delete(0, END)


def currPr():
    prPage = Tk()
    prPage.title('Personal records')
    prPage.geometry('600x500')

    #create a database or connect to one
    conn = sqlite3.connect('workout_log.db')
    #create a cursor
    c = conn.cursor()

    c.execute("SELECT *, oid FROM workouts")
    records = c.fetchall()

    pool = {}
    print_records = ""
    for record in records:
        if record[1] not in pool:
            pool[record[1]] = record[2]
        else:
            if pool[record[1]] < record[2]:
                pool[record[1]] = record[2]

    for key, value in pool.items():
        print_records += f"{key:<20} {value:<10}" + "\n"

    pr_label = Label(prPage, text= print_records, justify=CENTER)
    pr_label.grid(row = 1, column = 0, columnspan=6, pady=10)

    #commit changes to database
    conn.commit()

    #close connection
    conn.close()


def getByDate():

    #create a database or connect to one
    conn = sqlite3.connect('workout_log.db')
    #create a cursor
    c = conn.cursor()

    date_id = date_box.get()

    c.execute("SELECT date, exercise, weight, set_num, reps, oid FROM workouts WHERE date = ?", (date_id,))
    records = c.fetchall()

    query_label.config(text="")

    print_records = ""
    for record in records:
        formatted_record = f"Date: {record[0]:<15} Exercise: {record[1]:<20} Weight: {record[2]:<10} Set number: {record[3]:<10} Reps: {record[4]:<5} ID: {record[5]}"
        print_records += formatted_record + "\n"

    query_label.config(text=print_records)
    #query_label.grid(row = 13, column = 0, columnspan=6, pady=10)

    #commit changes to database
    conn.commit()
    #close connection
    conn.close()


#create query function
def query():
    global query_label
    global date_box
    global popup
    popup = Tk()
    popup.title('records')
    popup.geometry('600x500')

    #create a database or connect to one
    conn = sqlite3.connect('workout_log.db')
    #create a cursor
    c = conn.cursor()

    #query the database
    c.execute("SELECT *, oid FROM workouts")
    records = c.fetchall()

    #loop through results
    print_records = ""
    for record in records:
        formatted_record = f"Date: {record[0]:<15} Exercise: {record[1]:<20} Weight: {record[2]:<10} Set number: {record[3]:<10} Reps: {record[4]:<5} ID: {record[5]}"
        print_records += formatted_record + "\n"

    query_label = Label(popup, text= print_records, justify=CENTER)
    query_label.grid(row = 13, column = 0, columnspan=6, pady=10)

    date_box = Entry(popup, width = 20)
    date_box.grid(row = 14, column= 1, pady=5)
    date_box_label = Label(popup, text= 'Select date')
    date_box_label.grid(row = 14, column = 0, pady=5)
    by_date_button = Button(popup, text= 'show records by date', justify=CENTER, command= getByDate)
    by_date_button.grid(row = 15, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 136)

    #commit changes to database
    conn.commit()

    #close connection
    conn.close()


#create text boxes
date = Entry(root, width = 30)
date.grid(row = 0, column = 1, padx = 20, pady = (10,0))
exercise = Entry(root, width = 30)
exercise.grid(row = 1, column = 1)
weight = Entry(root, width = 30)
weight.grid(row = 2, column = 1)
set_num = Entry(root, width = 30)
set_num.grid(row = 3, column = 1)
reps = Entry(root, width = 30)
reps.grid(row = 4, column = 1)

delete_box = Entry(root, width = 20)
delete_box.grid(row = 9, column= 1, pady=5)


#create text box labels
date_label = Label(root, text= 'Date')
date_label.grid(row = 0, column = 0, pady = (10,0))
exercise_label = Label(root, text= 'Exercise name')
exercise_label.grid(row = 1, column = 0)
weight_label = Label(root, text='Weight (lbs)')
weight_label.grid(row = 2, column = 0)
set_num_label = Label(root, text= 'Set number')
set_num_label.grid(row = 3, column = 0)
reps_label = Label(root, text='Number of reps')
reps_label.grid(row = 4, column = 0)

delete_box_label = Label(root, text= 'Select ID')
delete_box_label.grid(row = 9, column = 0, pady=5)

#create submit button
submit_button = Button(root, text= 'Add record to database', command=submit)
submit_button.grid(row=6, column= 0, columnspan = 2, pady = 10, padx = 10, ipadx = 110)

#create a query button
query_button = Button(root, text='Show records', command= query)
query_button.grid(row = 7, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 135)

#create a delete button
delete_button = Button(root, text='Delete record', command= delete)
delete_button.grid(row = 11, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 136)

#create a edit button
edit_button = Button(root, text='Edit record', command= edit)
edit_button.grid(row = 12, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 142)

pr_button = Button(root, text='PR check', command= currPr)
pr_button.grid(row = 13, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 147)

#commit changes to database
conn.commit()

#close connection
conn.close()

root.mainloop()