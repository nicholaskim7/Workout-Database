from tkinter import *
import random
import sqlite3

root = Tk()
root.title('workouts')
root.geometry('650x500')
root.configure(background='gray25')

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
    editor.configure(background='gray25')

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
    date_editor = Entry(editor, width = 30, bg= 'gray32')
    date_editor.grid(row = 0, column = 1, padx = 20, pady = (10,0))
    exercise_editor = Entry(editor, width = 30, bg= 'gray32')
    exercise_editor.grid(row = 1, column = 1)
    weight_editor = Entry(editor, width = 30, bg= 'gray32')
    weight_editor.grid(row = 2, column = 1)
    set_num_editor = Entry(editor, width = 30, bg= 'gray32')
    set_num_editor.grid(row = 3, column = 1)
    reps_editor = Entry(editor, width = 30, bg= 'gray32')
    reps_editor.grid(row = 4, column = 1)

    #create text box labels
    date_editor_label = Label(editor, text= 'Date', bg= 'gray25', fg= 'white')
    date_editor_label.grid(row = 0, column = 0, pady = (10,0))
    exercise_editor_label = Label(editor, text= 'Exercise name', bg= 'gray25', fg= 'white')
    exercise_editor_label.grid(row = 1, column = 0)
    weight_editor_label = Label(editor, text='Weight (lbs)', bg= 'gray25', fg= 'white')
    weight_editor_label.grid(row = 2, column = 0)
    set_num_editor_label = Label(editor, text= 'Set number', bg= 'gray25', fg= 'white')
    set_num_editor_label.grid(row = 3, column = 0)
    reps_editor_label = Label(editor, text='Number of reps', bg= 'gray25', fg= 'white')
    reps_editor_label.grid(row = 4, column = 0)

    #loop through results
    for record in records:
        date_editor.insert(0, record[0])
        exercise_editor.insert(0, record[1])
        weight_editor.insert(0, record[2])
        set_num_editor.insert(0, record[3])
        reps_editor.insert(0, record[4])

    #create a save button
    edit_button = Button(editor, text='Save record', command= update, bg= 'gray32', fg= 'white')
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
    prPage.geometry('500x400')
    prPage.configure(background='gray25')

    #create a database or connect to one
    conn = sqlite3.connect('workout_log.db')
    #create a cursor
    c = conn.cursor()

    c.execute("SELECT exercise, weight FROM workouts")
    records = c.fetchall()

    max_weights = {}
    for record in records:
        workout_name = record[0]
        weight = int(record[1])

        if workout_name not in max_weights or max_weights[workout_name] < weight:
            max_weights[workout_name] = weight

    print_records = ""
    for key, value in max_weights.items():
        print_records += f"{key:<20} {value:<10}\n"

    pr_label = Label(prPage, text= print_records, justify=CENTER, bg= 'gray32', fg= 'white')
    pr_label.grid(row = 1, column = 0, columnspan=6, pady=10)
    pr_label.configure(font=("Comic Sans MS", 11))

    #commit changes to database
    conn.commit()

    #close connection
    conn.close()


#randomized daily quote function
def quote():
    #create a database or connect to one
    conn = sqlite3.connect('workout_log.db')
    #create a cursor
    c = conn.cursor()

    quotes = ["Opportunities don't come knocking at the door. They present themselves when you knock the door down.", 
              "Perseverance will always override potential.", "Take what's yours. You can't expect someone else to give it to you.", 
              "Perseverance: every day showing up hitting your dues.", "Progression is the key to happiness.",
              "When you have a belief in something, then all of a sudden what you're doing actually has purpose and that makes it very valuable.",
              "Plant those seeds in the ground that you want to bear fruits from."]
    
    random_quote = random.choice(quotes)

    quote_label = Label(root, text= random_quote, justify=CENTER, bg= 'gray25', fg= 'white', wraplength=500)
    quote_label.grid(row = 14, column = 0, columnspan=6, pady=10)
    quote_label.configure(font= ("Comic Sans MS", 12))

    #commit changes to database
    conn.commit()
    #close connection
    conn.close()
quote()


def getByDate():

    #create a database or connect to one
    conn = sqlite3.connect('workout_log.db')
    #create a cursor
    c = conn.cursor()

    date_id = date_box.get()

    c.execute("SELECT date, exercise, weight, set_num, reps, oid FROM workouts WHERE date = ?", (date_id,))
    records = c.fetchall()

    #query_label.config(text="")
    text_widget.delete('1.0', END)

    
    for record in records:
        formatted_record = f"Date: {record[0]:<15} Exercise: {record[1]:<20} Weight: {record[2]:<10} Set number: {record[3]:<10} Reps: {record[4]:<5} ID: {record[5]}"
        text_widget.insert(END, formatted_record + "\n")
        text_widget.insert(END, "-"*70 + "\n")

    #query_label.config(text=print_records)
    #query_label.grid(row = 13, column = 0, columnspan=6, pady=10)

    #commit changes to database
    conn.commit()
    #close connection
    conn.close()


#create query function
def query():
    global text_widget
    #global query_label
    global date_box
    global popup
    popup = Tk()
    popup.title('records')
    popup.geometry('600x500')
    popup.configure(background='gray25')

    #frame for text
    text_frame = Frame(popup)
    text_frame.pack(fill=BOTH, expand= 0)

    #scroll bar
    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side = RIGHT, fill= Y)

    # Add a text widget to the frame
    text_widget = Text(text_frame, yscrollcommand=scrollbar.set)
    text_widget.pack(fill=BOTH, expand=1)
    
    # Configure the scrollbar to work with the text widget
    scrollbar.config(command=text_widget.yview)

    #frame for date entry query
    date_frame = Frame(popup, bg='gray25')
    date_frame.pack(fill=X)

    date_box = Entry(date_frame, width = 20, bg= 'gray32')
    date_box.grid(row = 0, column= 1, pady=5)
    date_box_label = Label(date_frame, text= 'Select date', bg= 'gray25', fg= 'sky blue')
    date_box_label.grid(row = 0, column = 0, pady=5)
    date_box_label.config(font= ('Arial', 10))

    by_date_button = Button(date_frame, text= 'show records by date', justify=CENTER, command= getByDate, bg= 'gray32', fg= 'white')
    by_date_button.grid(row = 1, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 136)



    #create a database or connect to one
    conn = sqlite3.connect('workout_log.db')
    #create a cursor
    c = conn.cursor()

    #query the database
    c.execute("SELECT *, oid FROM workouts")
    records = c.fetchall()

    #loop through results
    for record in records:
        formatted_record = f"Date: {record[0]:<15} Exercise: {record[1]:<20} Weight: {record[2]:<10} Set number: {record[3]:<10} Reps: {record[4]:<5} ID: {record[5]}"
        #print_records += formatted_record + "\n"
        text_widget.insert(END, formatted_record+ "\n")
        text_widget.insert(END, "-"*70+"\n")

    # query_label = Label(popup, text= print_records, justify=CENTER, bg= 'gray32', fg= 'white')
    # query_label.grid(row = 13, column = 0, columnspan=6, pady=10)
    # query_label.configure(font= ("Comic Sans MS", 11))

    #commit changes to database
    conn.commit()

    #close connection
    conn.close()


#create text boxes
date = Entry(root, width = 30, bg= 'gray32')
date.grid(row = 0, column = 1, padx = 20, pady = (10,0))
exercise = Entry(root, width = 30, bg= 'gray32')
exercise.grid(row = 1, column = 1)
weight = Entry(root, width = 30, bg= 'gray32')
weight.grid(row = 2, column = 1)
set_num = Entry(root, width = 30, bg= 'gray32')
set_num.grid(row = 3, column = 1)
reps = Entry(root, width = 30, bg= 'gray32')
reps.grid(row = 4, column = 1)

delete_box = Entry(root, width = 20, bg= 'gray32')
delete_box.grid(row = 9, column= 1, pady=5)


#create text box labels
date_label = Label(root, text= 'Date', bg= 'gray25', fg= 'white')
date_label.grid(row = 0, column = 0, pady = (10,0))
exercise_label = Label(root, text= 'Exercise name', bg= 'gray25', fg= 'white')
exercise_label.grid(row = 1, column = 0)
weight_label = Label(root, text='Weight (lbs)', bg= 'gray25', fg= 'white')
weight_label.grid(row = 2, column = 0)
set_num_label = Label(root, text= 'Set number', bg= 'gray25', fg= 'white')
set_num_label.grid(row = 3, column = 0)
reps_label = Label(root, text='Number of reps', bg= 'gray25', fg= 'white')
reps_label.grid(row = 4, column = 0)

delete_box_label = Label(root, text= 'Select ID', fg= 'sky blue', bg= 'gray25')
delete_box_label.grid(row = 9, column = 0, pady=5)
delete_box_label.config(font= ('Arial', 10))

#create submit button
submit_button = Button(root, text= 'Add record to database', command=submit, bg= 'gray32', fg= 'white')
submit_button.grid(row=6, column= 0, columnspan = 2, pady = 10, padx = 10, ipadx = 109)

#create a query button
query_button = Button(root, text='Show records', command= query, bg= 'gray32', fg= 'white')
query_button.grid(row = 7, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 135)

#create a delete button
delete_button = Button(root, text='Delete record (select id)', command= delete, bg= 'gray32', fg= 'white')
delete_button.grid(row = 11, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 109)

#create a edit button
edit_button = Button(root, text='Edit record (select id)', command= edit, bg= 'gray32', fg= 'white')
edit_button.grid(row = 12, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 115)

pr_button = Button(root, text='PR check', command= currPr, bg= 'gray32', fg= 'white')
pr_button.grid(row = 13, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 147)

#commit changes to database
conn.commit()

#close connection
conn.close()

root.mainloop()
