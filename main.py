import mysql.connector
import pandas as pd
import pyodbc

# Database connection settings for MySQL
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="emp"
)

cursor = con.cursor()
cursor = con.cursor(buffered= True)

# Function to check if an employee exists
def check_employee(employee_id):
    sql = 'SELECT * FROM employees WHERE id=%s'
    cursor.execute(sql, (employee_id,))
    return cursor.rowcount == 1

# Function to add an employee
def add_employee():
    Id = input("Enter Employee Id: ")
    if check_employee(Id):
        print("Employee already exists. Please try again.")
        
    
    Name = input("Enter Employee Name: ")
    Post = input("Enter Employee Post: ")
    Salary = input("Enter Employee Salary: ")
    Start_date = input("Enter Employee Start Date: ")

    sql = 'INSERT INTO employees (id, name, post, salary, start_date) VALUES (%s, %s, %s, %s, %s)'
    data = (Id, Name, Post, Salary, Start_date)
    try:
        
        cursor.execute(sql, data)
        con.commit()
        print("Employee Added Successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        con.rollback()

# Function to remove an employee
def remove_employee():
    Id = input("Enter Employee Id: ")
    if not check_employee(Id):
        print("Employee does not exist. Please try again.")
        return
    
    sql = 'DELETE FROM employees WHERE id=%s'
    data = (Id,)
    try:
        cursor.execute(sql, data)
        con.commit()
        print("Employee Removed Successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        con.rollback()

# Function to promote an employee
def promote_employee():
    Id = input("Enter Employee's Id: ")
    if not check_employee(Id):
        print("Employee does not exist. Please try again.")
        return
    
    try:
        Amount = float(input("Enter increase in Salary: "))

        sql_select = 'SELECT salary FROM employees WHERE id=%s'
        cursor.execute(sql_select, (Id,))
        current_salary = cursor.fetchone()[0]
        new_salary = current_salary + Amount

        sql_update = 'UPDATE employees SET salary=%s WHERE id=%s'
        cursor.execute(sql_update, (new_salary, Id))
        con.commit()
        print("Employee Promoted Successfully")

    except (ValueError, mysql.connector.Error) as e:
        print(f"Error: {e}")
        con.rollback()

# Function to display all employees
def display_employees():
    try:
        sql = 'SELECT * FROM employees'
        cursor.execute(sql)
        employees = cursor.fetchall()
        for employee in employees:
            print("Employee Id : ", employee[0])
            print("Employee Name : ", employee[1])
            print("Employee Post : ", employee[2])
            print("Employee Salary : ", employee[3])
            print("Employee Start Date: ", employee[4])
            print("------------------------------------")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

#Function to change employee details
def change_employee_date():
    Id = input("Enter Employee Id: ")
    if not check_employee(Id):
        print("Employee does not exist. Please try again.")
        return

    while True:
        print("\nSelect one of the following options to change the records: ")
        print("Press:")
        print("1 to Change Employee ID")
        print("2 to Change Employee Name")
        print("3 to Change Employee Post")
        print("4 to Change Employee Salary")
        print("5 to Change Employee Start Date")
        print("6 to Exit")


        ch = input("Enter your choice: ")

        if ch == '1':
            emp_id = input("Enter New Employee ID: ")

            #Update the employee id with sql query

            sql = "UPDATE employees SET id = %s WHERE id = %s"
            data = (emp_id, Id)
            try:

                cursor.execute(sql, data)
                con.commit()
                print("Employe ID Updated Successfully.")
            
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                con.rollback

        if ch == '2':
            emp_name = input("Enter New Employee Name: ")

            #Update the employee name with sql query
            sql = "UPDATE employees SET name = %s WHERE id = %s"
            data = (emp_name, Id)
            try:

                cursor.execute(sql, data)
                con.commit()
                print("Employe Name Updated Successfully.")
            
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                con.rollback
            pass

        if ch == '3':
            emp_post = input("Enter New Employee Post: ")

            #Update the employee post with sql query
            sql = "UPDATE employees SET post = %s WHERE id = %s"
            data = (emp_post, Id)
            try:

                cursor.execute(sql, data)
                con.commit()
                print("Employe Post Updated Successfully.")
            
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                con.rollback


        if ch == '4':
            emp_salary = input("Enter New Employee Salary: ")

            #Update the employee name with sql query
            sql = "UPDATE employees SET salary = %s WHERE id = %s"
            data = (emp_salary, Id)
            try:

                cursor.execute(sql, data)
                con.commit()
                print("Employe Salary Updated Successfully.")
            
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                con.rollback

        if ch == '5':
            emp_start_date = input("Enter New Employee Start Date: ")

            #Update the employee name with sql query
            sql = "UPDATE employees SET start_date = %s WHERE id = %s"
            data = (emp_start_date, Id)
            try:

                cursor.execute(sql, data)
                con.commit()
                print("Employe Start Date Updated Successfully.")
            
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                con.rollback
            
        if ch == '6':
            break
# Function to display the menu

def export_to_csv():
    
    server_name ='[localhost]'
    database_name = '[emp]'
    export_path = ['employees.csv']

    connection_string = 'DRIVER={localhost};SERVER='+server_name+';DATABASE='+database_name+';TRUSTED_CONNECTION=yes'
    connection = pyodbc.connect(connection_string)
    query = '''
    SELECT * 
    FROM emp.employees
    '''

    data = pd.read_sql(query, connection)
    data.to.csv(export_path, index=False)

def menu():
    while True:
        print("\nWelcome to Employee Management Record")
        print("Press:")
        print("1 to Add Employee")
        print("2 to Remove Employee")
        print("3 to Promote Employee")
        print("4 to Display Employees")
        print("5 to Change Employee Data")
        print("6 to exit.")
        
        ch = input("Enter your Choice: ")

        if ch == '1':
            add_employee()
        elif ch == '2':
            remove_employee()
        elif ch == '3':
            promote_employee()
        elif ch == '4':
            display_employees()
        elif ch == '5':
            export_to_csv()
        elif ch == '6':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid Choice! Please try again.")

if __name__ == "__main__":
    menu()
