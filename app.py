from flask import Flask, render_template, request, redirect
import sqlite3
import os
import webbrowser
from threading import Timer

app = Flask(__name__)

# Database path - works on both local and Vercel
if os.environ.get('VERCEL'):
    DB_PATH = '/tmp/expenses.db'
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), 'expenses.db')

# Initialize DB
def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute('''CREATE TABLE IF NOT EXISTS expenses
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT,
                     amount REAL)''')
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

init_db()

# Home page
@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    expenses = conn.execute('SELECT * FROM expenses').fetchall()
    
    total = sum([row[2] for row in expenses])
    
    conn.close()
    return render_template('index.html', expenses=expenses, total=total)

# Add expense
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    amount = request.form['amount']

    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO expenses (title, amount) VALUES (?, ?)", (title, amount))
    conn.commit()
    conn.close()

    return redirect('/')

# Delete expense
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

def open_browser():
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # Open browser after 1 second
    timer = Timer(1, open_browser)
    timer.daemon = True
    timer.start()
    
    app.run(debug=True)