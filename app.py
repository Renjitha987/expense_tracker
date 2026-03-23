from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT,
                 amount REAL)''')
    conn.close()

init_db()

# Home page
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    expenses = conn.execute('SELECT * FROM expenses').fetchall()
    
    total = sum([row[2] for row in expenses])
    
    conn.close()
    return render_template('index.html', expenses=expenses, total=total)

# Add expense
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    amount = request.form['amount']

    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO expenses (title, amount) VALUES (?, ?)", (title, amount))
    conn.commit()
    conn.close()

    return redirect('/')

# Delete expense
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)