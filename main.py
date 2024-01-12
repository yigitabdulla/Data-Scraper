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
    
    # Reading data from text file and neatly creating dictionary
    with open('modified_data2.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        parts = line.strip().split(';')

        if(len(parts) > 23):
            print(parts)

        car = {
            'model': parts[0],
            'brand': parts[1],
            'price': parts[2],
            'foreign_currency': parts[3],
            'date_of_currency': parts[4],
            'gear': parts[5],
            'fuel': parts[6],
            'engine_displacement': parts[7],
            'transmission': parts[8],
            'horsepower': parts[9],
            'mortgage': parts[10],
            'confiscation': parts[11],
            'inspection': parts[12],
            'year': parts[13],
            'km': parts[14],
            'area_of_use': parts[15],
            'colour': parts[16],
            'top_speed': parts[17],
            'luggage_volume': parts[18],
            '0-100': parts[19],
            'max_torque': parts[20],
            'cylinder': parts[21],
            'tank': parts[22],
            'consumption': parts[23],
            'valve': parts[24]
        }

        data.append(car)
    print(data[24])
    
    # Creating a TKinter window
    root = tk.Tk()
    root.title("Second Hand Car App")
    input_frame = tk.Frame(root)
    input_frame.pack()
    
    def search_data():
        search_term = search_entry.get().strip().lower()

        if not search_term:
            return  # If the search term is empty, do not take action

        # Clear filtered data
        for i in treeview.get_children():
            treeview.delete(i)

        # Search by brand or model
        filtered_cars = [car for car in data if
                        search_term in car['brand'].lower() or
                        search_term in car['model'].lower() or
                        (search_term in f"{car['brand'].lower()} {car['model'].lower()}")]

        # Show filtered data
        if filtered_cars:
            for car in filtered_cars:
                values = [car.get(col.replace(' ', '_').lower(), '') for col in columns]
                treeview.insert('', 'end', values=values)
        else:
            treeview.insert('', 'end', values=["No matching data found"])
        
        # Search entry
    search_entry = tk.Entry(input_frame)
    search_entry.pack(side=tk.LEFT)

    # Search button
    search_button = tk.Button(input_frame, text="Search", command=search_data)
    search_button.pack(side=tk.LEFT, padx=(5, 200))
