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

    # Brand filtering
    brand = ['All'] + list(set(car['brand'] for car in data))
    brand_var = tk.StringVar(root)
    brand_var.set(brand[0])  # Select "All" brand initially
    brand_label = tk.Label(input_frame, text="Brand:")
    brand_label.pack(side=tk.LEFT)

    brand_dropdown = tk.OptionMenu(input_frame, brand_var, *brand)
    brand_dropdown.pack(side=tk.LEFT)

    # Model filtering
    model = list(set(car['model'] for car in data))
    model_var = tk.StringVar(root)
    model_var.set("All")  # Select "All" model initially

    model_label = tk.Label(input_frame, text="Model:")
    model_label.pack(side=tk.LEFT)

    model_dropdown = tk.OptionMenu(input_frame, model_var, "All", *model)
    model_dropdown.pack(side=tk.LEFT)
    
    def update_models(*args):
        selected_brand = brand_var.get()
        models_for_selected_brand = list(set(car['model'] for car in data if car['brand'] == selected_brand))
        models_for_selected_brand.insert(0, "All")  # Show all models
        model_var.set("All")  # Initially selected "All"

        # Update model dropdown menu options
        menu = model_dropdown["menu"]
        menu.delete(0, "end")
        for model in models_for_selected_brand:
            menu.add_command(label=model, command=tk._setit(model_var, model))
    
        # Update models when brand selection changes
    brand_var.trace_add("write", update_models)

    # Year dropdown
    years = list(set(car['year'] for car in data))
    years.insert(0, "All")  # Added row: Show all years
    year_var = tk.StringVar(root)
    year_var.set("All")  # Changed line: "All" is initially selected

    year_label = tk.Label(input_frame, text="Filtering Year:")
    year_label.pack(side=tk.LEFT)

    year_dropdown = tk.OptionMenu(input_frame, year_var, *years)
    year_dropdown.pack(side=tk.LEFT)

    # Price Filtering
    price_label = tk.Label(input_frame, text="Price Range:")
    price_label.pack(side=tk.LEFT)

    min_price_label = tk.Label(input_frame, text="Min:")
    min_price_label.pack(side=tk.LEFT)

    min_price_entry = tk.Entry(input_frame)
    min_price_entry.pack(side=tk.LEFT)

    max_price_label = tk.Label(input_frame, text="Max:")
    max_price_label.pack(side=tk.LEFT)

    max_price_entry = tk.Entry(input_frame)
    max_price_entry.pack(side=tk.LEFT)

    # Filtering button
    filter_button = tk.Button(input_frame, text="Filter", command=filter_data)
    filter_button.pack(side=tk.LEFT)
    
    # Set the initial size of the window and make it nearly full-screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    initial_width = int(screen_width * 0.8)
    initial_height = int(screen_height * 0.8)
    initial_position_x = int((screen_width - initial_width) / 2)
    initial_position_y = int((screen_height - initial_height) / 2)
    
    def scrape_data(page_entry):
        
        driver = webdriver.Chrome()
        driver.maximize_window()
        
        try:
            page_value = int(page_entry.get())
            
            if page_value <= 0:
                messagebox.showerror("Error", "Please enter positive number")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

        for page in range(page_value, page_value + 1):
            driver.get("https://dod.com.tr/arac-arama?page=" + str(page))
            WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located(
                (By.CLASS_NAME, "do-search-result-table__container__cards")))
            cars = driver.find_elements(By.CLASS_NAME, 'do-vehicle-card__preview')
            car_links = []
            car_num = 1
            for car in cars:
                href = car.find_element(By.XPATH,
                                        "//*[@id='__layout']/div/div[3]/main/div[2]/div[2]/div[2]/div[3]/div/div[1]/div[" + str(
                                            car_num) + "]/div/div[1]/div/a").get_attribute('href')
                car_num += 1
                car_links.append(href)

            formatted_line = []

            for car in car_links:

                formatted_lines = []

                car_driver = webdriver.Chrome()
                car_driver.get(car)
                WebDriverWait(car_driver, 15).until(expected_conditions.visibility_of_element_located(
                    (By.CLASS_NAME, "do-vehicle-detail-primary-info__price-text")))

                price = car_driver.find_elements(By.CLASS_NAME, "do-vehicle-detail-primary-info__price-text")
                modal = car_driver.find_elements(By.CLASS_NAME, "do-vehicle-detail-primary-info__model")
                brand = car_driver.find_elements(By.CLASS_NAME, "do-vehicle-detail-primary-info__brand")
                details = car_driver.find_elements(By.CLASS_NAME,
                                                   "do-vehicle-detail-info-section__other-specs__item__value")
                info = car_driver.find_elements(By.CLASS_NAME,
                                                "do-vehicle-detail-info-section__featured-specs__item__body")
                ekspertiz = car_driver.find_elements(By.CLASS_NAME,
                                                     "do-vehicle-expert-report-section__description-item")
                formatted_lines.append(modal)
                formatted_lines.append(brand)
                formatted_lines.append(price)
                formatted_lines.append(info)
                formatted_lines.append(details)

                data = []
                for car_specs in formatted_lines:
                    for spec in car_specs:
                        value = spec.text
                        data.append(value)

                for i in range(3, 9):
                    data[i] = data[i].split("\n")[1]

                del data[8:12]

                data2 = []
                for rapor in ekspertiz:
                    data2.append(rapor.text)

                if (len(data2) > 0):
                    updated_list = [entry.replace('\n', ':') for entry in data2]
                    data = data + updated_list

                with open('output.txt', 'a', encoding='utf-8') as file:
                    file.write(';'.join(map(str, data)) + '\n')

                car_driver.close()
            converting_csv_file()
            # Reading data from text file and neatly creating dictionary
            with open('output.csv', 'r', encoding='utf-8') as file:
                lines = file.readlines()


            data = []

            for line in lines:
                parts = line.strip().split(';')
                parts.insert(3,"30.20")
                parts.insert(4,"21.01.2024")
                data.append(parts)

            # Writing modified data back to a new CSV file
            with open('modified_data2.csv', 'a', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerows(data)
        
        reopen_ui()
    
    def reopen_ui():
        root.destroy()
        open_main_ui(user_role)
        

    page_label = tk.Label(root, text="Page number:")
    page_label.pack()

    page_entry = tk.Entry(root)
    page_entry.pack()

    root.geometry(f"{initial_width}x{initial_height}+{initial_position_x}+{initial_position_y}")

    # Creating a data display widget (we will use Treeview)
    treeview = ttk.Treeview(root, columns=columns, show='headings')

    # Set column widths for each column
    column_widths = [60, 60, 100, 60, 60, 60, 100, 100, 80, 100, 80, 60, 60, 80, 80, 80, 100, 80, 80, 80, 60, 100, 60,
                     60]
    for col, width in zip(columns, column_widths):
        treeview.column(col, width=width, anchor=tk.CENTER)  # Adjust the anchor as needed

    # Adjust column headers
    for col in columns:
        treeview.heading(col, text=col)

    # Button for executing scraping
    scrape_button = tk.Button(root, text="Scrape Data", command=lambda: scrape_data(page_entry))
    # Conditionally disable the button based on user_role
    if user_role != "admin":
        scrape_button.config(state=tk.DISABLED)

    scrape_button.pack()

    def add_data():
    # Function to handle the "Add Data" button press

        def save_data():
            # Function to save data entered in the new window to the CSV file

            # Get values from entry widgets
            new_data = [entry.get() for entry in entry_widgets]

            # Check if any entry is empty
            if any(not value for value in new_data):
                messagebox.showwarning("Add Data", "Please fill in all fields.")
                return

            # Append new data to the CSV file
            with open('modified_data2.csv', 'a', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerow(new_data)
                
            # Show success message
            messagebox.showinfo("Add Data", "Data added successfully")

            # Close the data entry window  
            add_data_window.destroy()
            root.destroy()
            open_main_ui(user_role)

        # Create a new window for data entry
        add_data_window = tk.Toplevel(root)
        add_data_window.title("Add Data")

        # Create entry widgets for each column
        entry_widgets = []
        for col, column_name in enumerate(columns):
            tk.Label(add_data_window, text=f"{column_name}:").grid(row=col, column=0, padx=5, pady=4)
            entry = tk.Entry(add_data_window)
            entry.grid(row=col, column=1, padx=5, pady=5)
            entry_widgets.append(entry)

        # Create "Save" button
        save_button = tk.Button(add_data_window, text="Save Data", command=save_data)
        save_button.grid(row=len(columns), column=0, columnspan=2, pady=9)

    # Add Data button
    add_data_button = tk.Button(root, text="Add Data", command=add_data)
    
    if user_role != "admin":
        add_data_button.config(state=tk.DISABLED)
    
    add_data_button.pack()
    
    # Make the Treeview widget expand to fill available space
    treeview.pack(expand=True, fill=tk.BOTH)
    root.mainloop()

def register():
    username = entry_username_signup.get()
    password = entry_password_signup.get()
        
    # Check if the username exists in the user_info.txt file
    with open("user_info.txt", "r") as file:
        for line in file:
            stored_username, stored_password, role = line.strip().split(',')
            if username == stored_username:
                messagebox.showwarning("Registration Error","Username already exist!")
                return
    
    role = "user"
    
    if ("admin" in username):
        role = "admin"

    # Check if username or password is empty
    if not username or not password:
        messagebox.showwarning("Registration Error", "Please enter both username and password.")
        return

    if username in user_database:
            messagebox.showwarning("Registration Error","Username already exist!")
            return
        
    # Store the registration information in a text file
    with open("user_info.txt", "a") as file:
        file.write(f"{username},{password},{role}\n")

    # Store the registration information (you might want to use a database here)
    # For simplicity, storing in a dictionary in memory
    user_database[username] = password
    

    # Clear the registration entries
    entry_username_signup.delete(0, tk.END)
    entry_password_signup.delete(0, tk.END)

    messagebox.showinfo("Registration Successful", "You have successfully registered.")

def login():
    global user_role
    username = entry_username_login.get()
    password = entry_password_login.get()

    # Check if username or password is empty
    if not username or not password:
        messagebox.showwarning("Login Error", "Please enter both username and password.")
        return

    # Check if the username exists in the user_info.txt file
    with open("user_info.txt", "r") as file:
        for line in file:
            stored_username, stored_password, role = line.strip().split(',')
            if username == stored_username and password == stored_password:
                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                user_role = role
                root.destroy()

                # Open the main UI
                open_main_ui(username)

                # Close the login frame (optional)
                frame_login.pack_forget()
                return

    messagebox.showwarning("Login Error", "Username or password incorrect.")
    

# Create the main window
root = tk.Tk()
root.title("User Registration and Login")

# Frames
frame_signup = tk.Frame(root)
frame_signup.pack(padx=10, pady=10)

frame_login = tk.Frame(root)

# Initial frame
frame_signup.pack()

# Registration widgets
label_username_signup = tk.Label(frame_signup, text="Username:")
label_username_signup.grid(row=0, column=0, padx=5, pady=5)
entry_username_signup = tk.Entry(frame_signup)
entry_username_signup.grid(row=0, column=1, padx=5, pady=5)

label_password_signup = tk.Label(frame_signup, text="Password:")
label_password_signup.grid(row=1, column=0, padx=5, pady=5)
entry_password_signup = tk.Entry(frame_signup, show="*")
entry_password_signup.grid(row=1, column=1, padx=5, pady=5)

button_register = tk.Button(frame_signup, text="Register", command=register)
button_register.grid(row=2, column=0, columnspan=2, pady=10)

link_login = tk.Label(frame_signup, text="Already have an account? Login", fg="blue", cursor="hand2")
link_login.grid(row=3, column=0, columnspan=2, pady=5)
link_login.bind("<Button-1>", lambda event: switch_to_login())

# Login widgets
label_username_login = tk.Label(frame_login, text="Username:")
label_username_login.grid(row=0, column=0, padx=5, pady=5)
entry_username_login = tk.Entry(frame_login)
entry_username_login.grid(row=0, column=1, padx=5, pady=5)

label_password_login = tk.Label(frame_login, text="Password:")
label_password_login.grid(row=1, column=0, padx=5, pady=5)
entry_password_login = tk.Entry(frame_login, show="*")
entry_password_login.grid(row=1, column=1, padx=5, pady=5)

button_login = tk.Button(frame_login, text="Login", command=login)
button_login.grid(row=2, column=0, columnspan=2, pady=10)

link_signup = tk.Label(frame_login, text="Don't have an account? Sign Up", fg="blue", cursor="hand2")
link_signup.grid(row=3, column=0, columnspan=2, pady=5)
link_signup.bind("<Button-1>", lambda event: switch_to_signup())

# Dummy user database (replace with a database or more secure storage)
user_database = {}

# Start the Tkinter main loop
root.mainloop()
