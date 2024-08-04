import tkinter as tk
from tkinter import messagebox
import sqlite3


def create_db():
    conn = sqlite3.connect('calculator.db')
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS history''')
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  expression TEXT,
                  result REAL)''')
    conn.commit()
    conn.close()


def insert_history(expression, result):
    conn = sqlite3.connect('calculator.db')
    c = conn.cursor()
    c.execute('INSERT INTO history (expression, result) VALUES (?, ?)', (expression, result))
    conn.commit()
    conn.close()


def fetch_history():
    conn = sqlite3.connect('calculator.db')
    c = conn.cursor()
    c.execute('SELECT * FROM history')
    history = c.fetchall()
    conn.close()
    return history


def perform_calculation():
    try:
        expression = text_box.get("1.0", tk.END).strip()
        result = eval(expression)
        insert_history(expression, result)
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, str(result))
    except Exception as e:
        messagebox.showerror("Error", f"Invalid expression: {e}")

def update_entry(char):
    current_text = text_box.get("1.0", tk.END).strip()
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, current_text + char)

def clear_entry():
    text_box.delete("1.0", tk.END)

def show_history():
    history = fetch_history()
    history_window = tk.Toplevel(root)
    history_window.title("Calculation History")

    for i, record in enumerate(history):
        tk.Label(history_window, text=f"{record[1]} = {record[2]}").grid(row=i, column=0, padx=10, pady=5)

root = tk.Tk()
root.title("Simple Calculator")

text_box = tk.Text(root, width=30, height=2, borderwidth=5, font=('Arial', 14))
text_box.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
    ('0', 4, 0), ('C', 4, 1), ('=', 4, 2), ('/', 4, 3)
]

for (text, row, col) in buttons:
    if text == '=':
        action = perform_calculation
    elif text == 'C':
        action = clear_entry
    else:
        action = lambda x=text: update_entry(x)
    tk.Button(root, text=text, padx=10, pady=10, font=('Arial', 14), command=action, bg="light blue").grid(row=row, column=col, padx=5, pady=5)

tk.Button(root, text="Show History", command=show_history, padx=10, pady=10, font=('Arial', 14), bg="light gray").grid(row=5, column=0, columnspan=4, padx=5, pady=5)

create_db()
root.mainloop()