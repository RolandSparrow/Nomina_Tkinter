from distutils.command import config
from tkinter import ttk
from tkinter import *


import sqlite3



class Empleado:
    # connection dir property
    db_name = 'database.db'

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('register employees')

        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Register new employee')
        frame.grid(row = 0, column = 0, columnspan = 10, pady = 20)

        # Name Input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)        
        
        #Last Name Input
        Label(frame, text ='Last Name: ').grid(row = 1, column = 3)
        self.last_name = Entry(frame)
        self.last_name.grid(row = 1, column = 4)
        
        #Id Input
        Label(frame, text= 'identification card:').grid(row = 3, column = 0)
        self.id = Entry(frame)
        self.id.grid(row = 3, column =1)
        
        #Salary Input 
        Label(frame, text= 'Salary:').grid(row = 3, column = 3)
        self.salary = Entry(frame)
        self.salary.grid(row = 3, column = 4)
        
        #days Input
        Label(frame, text= 'Days: ').grid(row = 5, column = 0)
        self.days = Entry(frame)
        self.days.grid(row = 5, column = 1)    

        # Button Add Employee 
        ttk.Button(frame, text = 'Save Employee', command = self.add_employee).grid(row = 6, columnspan = 6)
        
        

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 6, column = 0, columnspan = 2, sticky = W + E)

        # Table
        columns = ('#0', '#1', '#2', '#3')
        self.tree = ttk.Treeview(height = 10, columns = columns) 
        self.tree.grid(row = 7, column = 0, columnspan =10)      
        self.tree.heading('#0', text='Name', anchor = CENTER )
        self.tree.heading('#1', text ='Last Name', anchor = CENTER)
        self.tree.heading('#2', text='identification', anchor = CENTER )
        self.tree.heading('#3', text ='Salary', anchor = CENTER)
        self.tree.heading('#4', text ='Days', anchor = CENTER)
        


        # Buttons
        ttk.Button(text = 'DELETE', command = self.delete_employee).grid(row = 8, column = 2,columnspan=8)
        ttk.Button(text = 'EDIT', command = self.edit_employee).grid(row = 8, column = 1,columnspan=6)

        # Filling the Rows
        self.get_employee()

    # Function to Execute Database Query
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get employee from Database
    def get_employee(self):
        # cleaning Table 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM Employee ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert("", 0, text = row[1], values = (row[2], row[3], row[4], row[5]))         
    # User Input Validation
    def validation(self):
        return len(self.name.get()) != 0 and len(self.last_name.get()) != 0 and len(self.id.get()) != 0 and len(self.salary.get()) != 0 and len(self.days.get()) != 0

    def add_employee(self):
        if self.validation():
            query = 'INSERT INTO Employee VALUES(NULL, ?, ?, ?, ?, ?)'
            parameters =  (self.name.get(), self.last_name.get(),self.id.get(),self.salary.get(),self.days.get())
            self.run_query(query,parameters)
            self.message['text'] = 'Employee {} added Successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.last_name.delete(0, END)
            self.id.delete(0, END)
            self.salary.delete(0, END)
            self.days.delete(0, END)
        else:
            self.message['text'] = 'Required'
            self.get_employee()

    def delete_employee(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Employee WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_employee()

    def edit_employee(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return
        name = self.tree.item(self.tree.selection())['text']
        last_name = self.tree.item(self.tree.selection())['values'][0]
        id = self.tree.item(self.tree.selection())['values'][1]
        salary = self.tree.item(self.tree.selection())['values'][2]
        days = self.tree.item(self.tree.selection())['values'][3]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Employee'
        
        # Old Name
        Label(self.edit_wind, text = 'Old Name:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'New Name:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # Old Last Name
        Label(self.edit_wind, text = 'Old Last_Name:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = last_name), state = 'readonly').grid(row = 2, column = 2)
        # New Last Name
        Label(self.edit_wind, text = 'New Last_Name:').grid(row = 3, column = 1)
        new_last_name = Entry(self.edit_wind)
        new_last_name.grid(row = 3, column = 2)
        
        # Old id
        Label(self.edit_wind, text = 'Old Id:').grid(row = 4, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = id), state = 'readonly').grid(row = 4, column = 2)
        # New id
        Label(self.edit_wind, text = 'New Id:').grid(row = 5, column = 1)
        new_id = Entry(self.edit_wind)
        new_id.grid(row = 5, column = 2)
                              
        # Old Salary 
        Label(self.edit_wind, text = 'Old Salary:').grid(row = 6, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = salary), state = 'readonly').grid(row = 6, column = 2)
        # New Salary
        Label(self.edit_wind, text = 'New Salary:').grid(row = 7, column = 1)
        new_salary= Entry(self.edit_wind)
        new_salary.grid(row = 7, column = 2)
        
        # Old Days
        Label(self.edit_wind, text = 'Old Days:').grid(row = 8, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = days), state = 'readonly').grid(row = 8, column = 2)
        # New Days
        Label(self.edit_wind, text = 'New Days:').grid(row = 9, column = 1)
        new_days = Entry(self.edit_wind)
        new_days.grid(row = 9, column = 2)

        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(new_name.get(), name, new_last_name.get(), last_name, new_id.get(), id, new_salary.get(), salary, new_days.get(), days)).grid(row = 10, column = 2, sticky = W + E)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_last_name, last_name, new_id, id, new_salary, salary, new_days, days):
        query = 'UPDATE Employee SET name = ?, last_name = ?, identification = ?, salary = ?, days = ? WHERE name = ? AND last_name = ?  AND identification = ?  AND salary = ?  AND days = ?'
        parameters = (new_name, name,new_last_name, last_name, new_id, id, new_salary, salary, new_days, days)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(name)
        self.get_employee()

if __name__ == '__main__':
    window = Tk()
    application = Empleado(window)
    window.mainloop()