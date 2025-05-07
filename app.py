from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

# Database initialization
def init_db():
    try:
        conn = sqlite3.connect('payroll.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                idno TEXT NOT NULL,
                lastname TEXT NOT NULL,
                firstname TEXT NOT NULL,
                position TEXT NOT NULL,
                rate_per_day REAL NOT NULL,
                days_work REAL DEFAULT 0.0,
                total REAL DEFAULT 0.0
            )
        ''')
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_db_connection():
    conn = sqlite3.connect('payroll.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_all_employees():
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()
    return employees

@app.route("/")
def index():
    employees = get_all_employees()
    return render_template("index.html", employees=employees)

@app.route("/add_employee", methods=['POST'])
def add_employee():
    try:
        conn = get_db_connection()
        idno = request.form['idno']
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        position = request.form['position']
        rate_per_day = float(request.form['rate_per_day'])
        
        conn.execute('INSERT INTO employees (idno, lastname, firstname, position, rate_per_day) VALUES (?, ?, ?, ?, ?)',
                    (idno, lastname, firstname, position, rate_per_day))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    except:
        return 'There was an error adding the employee'

@app.route("/update_workdays/<int:id>", methods=['POST'])
def update_workdays(id):
    try:
        conn = get_db_connection()
        days_work = float(request.form['days_work'])
        
        # Get the rate per day
        employee = conn.execute('SELECT rate_per_day FROM employees WHERE id = ?', (id,)).fetchone()
        rate_per_day = employee['rate_per_day']
        
        # Calculate total
        total = days_work * rate_per_day
        
        conn.execute('UPDATE employees SET days_work = ?, total = ? WHERE id = ?',
                    (days_work, total, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    except:
        return 'There was an error updating work days'

@app.route("/delete/<int:id>")
def delete_employee(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM employees WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    except:
        return 'There was an error deleting the employee'

# Initialize the database when the app starts
init_db()
    
if __name__=="__main__":
    app.run(debug=True)