import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from pymongo import MongoClient

class MongoDBForm:
    def __init__(self, root):
        self.root = root
        self.root.title("API Data Retrieval")
        self.root.geometry("1000x600")
        self.root.configure(bg='#ffffff')  # White background

        # MongoDB connection
        self.client = MongoClient("")
        self.db = self.client["pr"]
        self.collections= self.db.list_collection_names()
        print(self.collections)

        # Configure styles
        style = ttk.Style()
        style.theme_use("clam")  # Use a modern theme

        # Colors
        primary_color = '#008cba'  # Primary color similar to the website
        button_color = '#ff8000'  # Orange color for buttons
        nav_color = '#ff8000'  # Orange color for navigation bar
        text_color = '#000000'    # Black color for text
        white_color = '#ffffff'   # White color

        # Style configurations
        style.configure("TLabel", font=("Helvetica", 12), background=white_color, foreground=text_color)
        style.configure("TButton", font=("Helvetica", 12), padding=5, background=button_color, foreground=white_color)
        style.map("TButton", background=[('active', button_color)], foreground=[('active', white_color)])
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("TDateEntry", font=("Helvetica", 12))
        style.configure("TCombobox", font=("Helvetica", 12))
        style.configure("TFrame", background=white_color)
        style.configure("Nav.TFrame", background=nav_color)
        style.configure("Nav.TLabel", background=nav_color, foreground=white_color, font=("Helvetica", 12, 'bold'))

        # Navigation Bar
        nav_frame = ttk.Frame(root, style="Nav.TFrame", relief="raised", borderwidth=2, padding=(10, 10))
        nav_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        nav_frame.grid_columnconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(1, weight=1)

        title_label = ttk.Label(nav_frame, text="API Data Retrieval", style="Nav.TLabel", anchor='center')
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        nav_label = ttk.Label(nav_frame, text="Home", style="Nav.TLabel", anchor='e')
        nav_label.grid(row=0, column=1, padx=10, pady=10, sticky=tk.E)

        # Main Frame
        main_frame = ttk.Frame(root, padding="20 20 20 20", style="TFrame")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_rowconfigure(5, weight=10)
        main_frame.grid_rowconfigure(6, weight=1)
        main_frame.grid_rowconfigure(7, weight=1)

        # Center align the variables
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Start Date Entry
        self.start_label = ttk.Label(main_frame, text="Start Date:", style="TLabel")
        self.start_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.start_date = DateEntry(main_frame, width=12, background='orange', foreground='white', borderwidth=2)
        self.start_date.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # End Date Entry
        self.end_label = ttk.Label(main_frame, text="End Date:", style="TLabel")
        self.end_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.end_date = DateEntry(main_frame, width=12, background='orange', foreground='white', borderwidth=2)
        self.end_date.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Data Type Dropdown
        self.data_type_label = ttk.Label(main_frame, text="Table Name:", style="TLabel")
        self.data_type_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.data_type = ttk.Combobox(main_frame, values=["Karza API", "LMS API", "Noval API"], font=("Helvetica", 12))
        self.data_type.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.data_type.current(0)  # Set default value
        # self.data_type.bind("<<ComboboxSelected>>", self.update_subtype_options)

        # Retrieve Button
        self.retrieve_button = ttk.Button(main_frame, text="Retrieve Data", command=self.retrieve_data, style="TButton")
        self.retrieve_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N)

        # Text Area to Display Data
        self.data_text = tk.Text(main_frame, height=15, font=("Helvetica", 12), wrap=tk.WORD, padx=10, pady=10)
        self.data_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.data_text.config(state=tk.DISABLED)  # Start with text area disabled

        # Email Entry
        self.email_label = ttk.Label(main_frame, text="Email Address:", style="TLabel")
        self.email_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.email_entry = ttk.Entry(main_frame, font=("Helvetica", 12))
        self.email_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

        # Submit Button
        self.submit_button = ttk.Button(main_frame, text="Submit", command=self.submit_data, style="TButton")
        self.submit_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N)

        # Make widgets expand with window resize
        self.data_text.grid(sticky="nsew")
        
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)


    def retrieve_data(self):
        start_date = self.start_date.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date.get_date().strftime("%Y-%m-%d")
        data_type = self.data_type.get()
        # subtype = self.subtype.get()

        # Query MongoDB
        # Select the collection based on the data type
        collection = self.db.get_collection()
        

        # Create query filter
        query = {
            "request_time": {"$gte": start_date, "$lte": end_date}
        } #"subtype": subtype

        # Query MongoDB
        data = collection.find(query)

        data_str = ""
        for record in data:
            data_str += str(record) + "\n"

        # Display Data
        self.data_text.config(state=tk.NORMAL)
        self.data_text.delete("1.0", tk.END)
        self.data_text.insert(tk.END, data_str)
        self.data_text.config(state=tk.DISABLED)

    def submit_data(self):
        email = self.email_entry.get()
        data = self.data_text.get("1.0", tk.END).strip()

        if email and data:
            #add logic to send the email with the data.
            print(f"Sending data to {email}...")

if __name__ == "__main__":
    root = tk.Tk()
    app = MongoDBForm(root)
    root.mainloop()
