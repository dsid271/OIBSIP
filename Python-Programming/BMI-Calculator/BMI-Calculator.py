import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BMI_Calculator_GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("BMI Calculator")
        self.master.geometry("400x300")

        style = ttk.Style()
        style.theme_use('clam')  # Using 'clam' theme for a basic and clean appearance

        self.label_instructions = tk.Label(master, text="Enter your weight and height below:", font=('Segoe UI', 12))
        self.label_instructions.pack(pady=10)

        self.label_weight = tk.Label(master, text="Weight (kg):", font=('Segoe UI', 10))
        self.label_weight.pack()
        self.entry_weight = tk.Entry(master, font=('Segoe UI', 10))
        self.entry_weight.pack()

        self.label_height = tk.Label(master, text="Height (m):", font=('Segoe UI', 10))
        self.label_height.pack()
        self.entry_height = tk.Entry(master, font=('Segoe UI', 10))
        self.entry_height.pack()

        self.btn_calculate = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi, font=('Segoe UI', 10), bg='#0078D4', fg='white')
        self.btn_calculate.pack(pady=10)

        self.btn_view_history = tk.Button(master, text="View History", command=self.view_history, font=('Segoe UI', 10), bg='#0078D4', fg='white')
        self.btn_view_history.pack()

    def calculate_bmi(self):
        try:
            weight = float(self.entry_weight.get())
            height = float(self.entry_height.get())

            if weight <= 0 or height <= 0:
                messagebox.showerror("Error", "Weight and height must be positive values.")
                return

            bmi = weight / (height ** 2)
            category = self.classify_bmi(bmi)

            self.save_to_database(weight, height, bmi, category)

            result_text = f"Your BMI is: {bmi:.2f}\nCategory: {category}"
            messagebox.showinfo("BMI Result", result_text)

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numeric values.")

    def classify_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def save_to_database(self, weight, height, bmi, category):
        conn = sqlite3.connect('bmi_database.db')
        cursor = conn.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS user_data (id INTEGER PRIMARY KEY, weight REAL, height REAL, bmi REAL, category TEXT)')

        cursor.execute('INSERT INTO user_data (weight, height, bmi, category) VALUES (?, ?, ?, ?)', (weight, height, bmi, category))

        conn.commit()
        conn.close()

    def view_history(self):
        conn = sqlite3.connect('bmi_database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT weight, height, bmi, category FROM user_data')
        data = cursor.fetchall()

        conn.close()

        if not data:
            messagebox.showinfo("No Data", "No BMI data available.")
            return

        # Create a new window for history
        history_window = tk.Toplevel(self.master)
        history_window.title("BMI History")

        # Create a treeview to display the data
        tree = ttk.Treeview(history_window, columns=("Weight", "Height", "BMI", "Category"), show="headings", height=10, style='Treeview')
        tree.pack(pady=10)

        for col in ["Weight", "Height", "BMI", "Category"]:
            tree.heading(col, text=col)
            tree.column(col, width=80, anchor='center')

        for row_data in data:
            tree.insert("", "end", values=row_data)

        # Add a button for BMI trend analysis
        btn_analyze_trend = tk.Button(history_window, text="Analyze BMI Trend", command=self.analyze_bmi_trend, font=('Segoe UI', 10), bg='#0078D4', fg='white')
        btn_analyze_trend.pack(pady=10)

    def analyze_bmi_trend(self):
        conn = sqlite3.connect('bmi_database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT bmi FROM user_data')
        bmi_data = cursor.fetchall()

        conn.close()

        if not bmi_data:
            messagebox.showinfo("No Data", "No BMI data available for analysis.")
            return

        # Create a plot for BMI trend analysis
        plt.figure(figsize=(8, 6))
        plt.plot([i+1 for i in range(len(bmi_data))], [row[0] for row in bmi_data], marker='o', color='#0078D4')
        plt.title("BMI Trend Analysis", fontdict={'fontname': 'Segoe UI', 'fontsize': 12})
        plt.xlabel("Entry Number", fontdict={'fontname': 'Segoe UI', 'fontsize': 10})
        plt.ylabel("BMI", fontdict={'fontname': 'Segoe UI', 'fontsize': 10})
        plt.grid(True)

        # Display the plot in a new window
        trend_window = tk.Toplevel(self.master)
        trend_window.title("BMI Trend Analysis")

        canvas = FigureCanvasTkAgg(plt.gcf(), master=trend_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMI_Calculator_GUI(root)
    root.mainloop()
