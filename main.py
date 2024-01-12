import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

user_role = ""

def switch_to_login():
    frame_signup.pack_forget()
    frame_login.pack()

def switch_to_signup():
    frame_login.pack_forget()
    frame_signup.pack()

def open_main_ui(user_role):
    columns = [
    'Model', 'Brand', 'Price','Foreign Currency','Date of Currency', 'Gear', 'Fuel', 'Engine Displacement', 'Transmission', 'Horsepower', 'Mortgage',
    'Confiscation', 'Inspection', 'Year', 'Km', 'Area of Use', 'Colour',
    'Top Speed', 'Luggage Volume', '0-100', 'Max Torque', 'Cylinder', 'Tank', 'Consumption', 'Valve']

    def converting_csv_file():
        # Specify the encoding of your text file (e.g., 'utf-8', 'latin-1', etc.)
        file_encoding = 'utf-8'

        # Open the text file for reading with the specified encoding
        with open('output.txt', 'r', encoding=file_encoding) as txt_file:
            # Read the lines from the text file
            lines = txt_file.readlines()

        # Assuming your text data has some structure, for example, tab-separated values
        # Split each line into fields based on the separator (e.g., '\t' for tab-separated)
        data = [line.strip().split('\t') for line in lines]

        # Open a CSV file for writing
        with open('output.csv', 'w', newline='', encoding=file_encoding) as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)

            # Write the data to the CSV file
            csv_writer.writerows(data)
    
    def filter_data():
        selected_brand = brand_var.get()
        selected_year = year_var.get()

        # Get entered minimum and maximum prices
        min_price_str = min_price_entry.get().replace('₺', '').replace('.', '').replace(',', '')
        max_price_str = max_price_entry.get().replace('₺', '').replace('.', '').replace(',', '')

        try:
            # Convert cleaned price strings to float
            min_price = float(min_price_str) if min_price_str else float('-inf')
            max_price = float(max_price_str) if max_price_str else float('inf')
        except ValueError:
            # Handle the case where the entered prices are not valid floats
            treeview.delete(*treeview.get_children())  # Clear the Treeview
            treeview.insert('', 'end', values=["Invalid price values"])
            return

        # Convert selected year to integer
        try:
            selected_year = int(selected_year) if selected_year != "All" else None
        except ValueError:
            treeview.delete(*treeview.get_children())  # Clear the Treeview
            treeview.insert('', 'end', values=["Invalid year value"])
            return

        # Filter by selected brand, year, and price range
        if selected_brand == "All":
            filtered_cars = [car for car in data if
                            (selected_year is None or int(car['year']) == selected_year) and
                            min_price <= float(car['price'].replace('₺', '').replace('.', '').replace(',', '')) <= max_price]
        elif model_var.get() == "All":
            filtered_cars = [car for car in data if
                            car['brand'] == selected_brand and
                            (selected_year is None or int(car['year']) == selected_year) and
                            min_price <= float(car['price'].replace('₺', '').replace('.', '').replace(',', '')) <= max_price]
        else:
            filtered_cars = [car for car in data if
                            car['brand'] == selected_brand and
                            car['model'] == model_var.get() and
                            (selected_year is None or int(car['year']) == selected_year) and
                            min_price <= float(car['price'].replace('₺', '').replace('.', '').replace(',', '')) <= max_price]

        # Cleaning UI
        for i in treeview.get_children():
            treeview.delete(i)

        # Show filtered data in columns
        if filtered_cars:
            for car in filtered_cars:
                values = [car.get(col.replace(' ', '_').lower(), '') for col in columns]
                treeview.insert('', 'end', values=values)
        else:
            # If no matching data, show a message
            treeview.insert('', 'end', values=["No matching data found"])
