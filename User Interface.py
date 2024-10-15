import tkinter as tk
from tkinter import messagebox
import json
from MLPlus import MLPlusAlgorithm, HybridDatabase

class MLPlusApp:
    def __init__(self, master):
        self.master = master
        master.title("ML-Plus User Interface")
        
        # Initialize Database and Algorithm
        self.db = HybridDatabase()
        self.ml_algorithm = MLPlusAlgorithm()

        # Create UI Components
        self.label = tk.Label(master, text="Enter Key:")
        self.label.pack()

        self.key_entry = tk.Entry(master)
        self.key_entry.pack()

        self.label_value = tk.Label(master, text="Enter Value:")
        self.label_value.pack()

        self.value_entry = tk.Entry(master)
        self.value_entry.pack()

        self.insert_button = tk.Button(master, text="Insert Data", command=self.insert_data)
        self.insert_button.pack()

        self.query_button = tk.Button(master, text="Query Data", command=self.query_data)
        self.query_button.pack()

        self.result_area = tk.Text(master, height=10, width=50)
        self.result_area.pack()

    def insert_data(self):
        key = self.key_entry.get()
        value = self.value_entry.get()
        result = self.db.insert_data(key, value)
        self.result_area.insert(tk.END, result + "\n")
        self.key_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)

    def query_data(self):
        key = self.key_entry.get()
        result = self.db.query_data(key)
        self.result_area.insert(tk.END, result + "\n")
        self.key_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MLPlusApp(root)
    root.mainloop()
