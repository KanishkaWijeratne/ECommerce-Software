import tkinter as tk
import pymysql

# SQL Connection
connection = pymysql.connect(host="localhost", user="root", passwd="", database="inventorymanagement")
cursor = connection.cursor()

# Create the main window
root = tk.Tk()
root.title("ECommerce")

# TEMPORARY LABEL
temp_label_text = tk.StringVar()
temp_label = tk.Label(root, textvariable=temp_label_text)
temp_label.grid(row=0, column=0, padx=5, pady=5)

def disable_buttons():
    customer_button['state']=tk.DISABLED
    customer_search['state']=tk.DISABLED
    product_button['state']=tk.DISABLED
    product_search['state']=tk.DISABLED
    order_button['state']=tk.DISABLED
    order_search['state']=tk.DISABLED
    
def enable_buttons():
    customer_button['state']=tk.NORMAL
    customer_search['state']=tk.NORMAL
    product_button['state']=tk.NORMAL
    product_search['state']=tk.NORMAL
    order_button['state']=tk.NORMAL
    order_search['state']=tk.NORMAL

def show_temporary_label(message, error=False):
    temp_label_text.set(message)
    if error:
        temp_label.config(fg="red")
    else:
        temp_label.config(fg="green")
    temp_label.grid_remove()  # Use grid_remove to hide the label
    temp_label.grid(row=0, column=1, padx=5, pady=5)
    root.after(1500, hide_temporary_label)

def back_to_menu():
    print(root.winfo_children())
    for widget in root.winfo_children():
        if widget in [customer_button, customer_search, product_button, product_search, order_button, order_search, exit_button, back_button_main]:
            pass
        else:
            widget.destroy()
    enable_buttons()



def hide_temporary_label():
    temp_label.grid_remove()  
def clear_search_results():
    # Destroy all widgets in rows 8 and below (where search results are displayed)
    for widget in root.winfo_children():
        if widget.grid_info() and int(widget.grid_info()["row"]) >= 8:
            widget.destroy()
# Function to display search results
def display_search_results(results, header):
    clear_search_results()
    # Display header
    header_label = tk.Label(root, text=header)
    header_label.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky="w")

    # Display each row in labels
    for i, row in enumerate(results):
        for j, value in enumerate(row):
            result_label = tk.Label(root, text=f"{value}", padx=5, pady=5)
            result_label.grid(row=9 + i, column=j, padx=5, pady=5)



def add_customer():
    disable_buttons()
    #THIS IS CALLED IN add_customer
    def add_email(full_name):
        def on_email_button_click():
            user_input = email_entry.get()
            if isinstance(user_input, str) and 0 < len(user_input) <= 30:
                # EMAIL VARIABLE
                email = user_input
                # Insert customer data into customer table
                sql = f"INSERT INTO Customer(Email, FullName) VALUES ('{email}', '{full_name}')"
                cursor.execute(sql)
                connection.commit()
                print (f"Customer: {full_name} successfully added")
                # Destroy the label and entry for email
                email_label.destroy()
                email_entry.destroy()
                email_entry_button.destroy()
                enable_buttons()
            else:
                print("Invalid input. Please enter a string with less than 30 characters.")
                show_temporary_label("Invalid input. Please enter a string with less than 30 characters.", error=True)

        email_label = tk.Label(root, text="Enter Email:")
        email_label.grid(row=1, column=0, padx=5, pady=5)
        email_entry = tk.Entry(root, width=30)
        email_entry.grid(row=1, column=1, padx=5, pady=5)
        # Button to trigger action based on email input
        email_entry_button = tk.Button(root, text="Submit", command=on_email_button_click)
        email_entry_button.grid(row=1, column=2, padx=5, pady=5)

    def on_name_button_click():
        user_input = customer_entry.get()
        if isinstance(user_input, str) and 0 < len(user_input) <= 30:
            # Split the user input into first name and last name
            names = user_input.split()
            if len(names) >= 2:
                full_name = user_input
                add_email(full_name)
                # Destroy the labels and entry for customer name
                label.destroy()
                customer_entry.destroy()
                customer_entry_button.destroy()
                
            else:
                print("Please enter both first name and last name.")
                show_temporary_label("Please enter both first name and last name.", error=True)
        else:
            print("Invalid input. Please enter a string with less than 30 characters.")
            show_temporary_label("Invalid input. Please enter a string with less than 30 characters.", error=True)

    # Label and Entry for customer information
    label = tk.Label(root, text="Customer Name (First Last):")
    label.grid(row=0, column=0, padx=5, pady=5)
    customer_entry = tk.Entry(root, width=30)
    customer_entry.grid(row=0, column=1, padx=5, pady=5)

    # Button to trigger action based on customer input
    customer_entry_button = tk.Button(root, text="Submit", command=on_name_button_click)
    customer_entry_button.grid(row=0, column=2, padx=5, pady=5)
 

    


def add_product_name(field_name):
    disable_buttons()
    def on_product_button_click():
        user_input = product_entry.get()
        if isinstance(user_input, str) and 0 < len(user_input) <= 30:
            # PRODUCT NAME VARIABLE
            product_name = user_input
            # Destroy the label and entry for product name
            product_label.destroy()
            product_entry.destroy()
            product_entry_button.destroy()
            add_price(product_name)
        else:
            print("Invalid input. Please enter a string with less than 30 characters.")
            show_temporary_label("Invalid input. Please enter a string with less than 30 characters.", error=True)

    product_label = tk.Label(root, text="Enter " + field_name + ":")
    product_label.grid(row=2, column=0, padx=5, pady=5)
    product_entry = tk.Entry(root, width=30)
    product_entry.grid(row=2, column=1, padx=5, pady=5)
    # Button to trigger action based on product input
    product_entry_button = tk.Button(root, text="Submit", command=on_product_button_click)
    product_entry_button.grid(row=2, column=2, padx=5, pady=5)
     # Back button
    back_button = tk.Button(root, text="Back", command=back_to_menu)
    back_button.grid(row=8, column=0, pady=20)

#CALLED IN add_product_name
def add_price(product_name):

    def on_price_button_click():
        user_input = price_entry.get()
        # Validate amount
        try:
            price_test = float(user_input)
            product_price = price_test
            # Destroy the label and entry for product price
            price_label.destroy()
            price_entry.destroy()
            price_entry_button.destroy()
            add_prod_inventory(product_name, product_price)
        except ValueError:
            print("Invalid amount input")
            show_temporary_label("Invalid Input. Enter a float value.", error = True)

    price_label = tk.Label(root, text="Enter Product Price:")
    price_label.grid(row=3, column=0, padx=5, pady=5)
    price_entry = tk.Entry(root, width=30)
    price_entry.grid(row=3, column=1, padx=5, pady=5)
    # Button to trigger action based on product price input
    price_entry_button = tk.Button(root, text="Submit", command=on_price_button_click)
    price_entry_button.grid(row=3, column=2, padx=5, pady=5)
def add_prod_inventory(product_name, product_price):
    def on_price_button_click():
        user_input = prod_inv_entry.get()
        # Validate amount
        try:
            product_inventory = user_input
            # Check if updating product
            query = f"select * from product where ProductName = '{product_name}'"
            cursor.execute(query)
            rows = cursor.fetchall()
            if len(rows) == 1:
                sql = f"UPDATE product SET Price = '{product_price}', NumInStock = '{product_inventory}' WHERE ProductName = '{product_name}'"
                cursor.execute(sql)
                print(f"Product: {product_name} successfully updated")
            else:
                # Insert product data into product table
                sql = f"INSERT INTO product(ProductName, Price, NumInStock) VALUES ('{product_name}', '{product_price}', '{product_inventory}')"
                cursor.execute(sql)
                print(f"Product: {product_name} successfully added")
            connection.commit()
            # Destroy the label and entry for product price
            prod_inv_label.destroy()
            prod_inv_entry.destroy()
            prod_inv_entry_button.destroy()
            enable_buttons()
        except ValueError:
            print("Invalid amount input")
            show_temporary_label("Invalid Input. Enter a Integer.", error = True)

    prod_inv_label = tk.Label(root, text="Enter Product Inventory Amount:")
    prod_inv_label.grid(row=3, column=0, padx=5, pady=5)
    prod_inv_entry = tk.Entry(root, width=30)
    prod_inv_entry.grid(row=3, column=1, padx=5, pady=5)
    # Button to trigger action based on product price input
    prod_inv_entry_button = tk.Button(root, text="Submit", command=on_price_button_click)
    prod_inv_entry_button.grid(row=3, column=2, padx=5, pady=5)


def order_pressed():
    customer_id = None  # Variable to store the verified customer ID
    product_id = None  # Variable to store the verified product ID
    disable_buttons()
    def get_customer_id():
        nonlocal customer_id  # Declare as nonlocal to modify the outer scope variable
        custID_label = tk.Label(root, text="Enter Customer ID:")
        custID_label.grid(row=3, column=0, padx=5, pady=5)
        custID_entry = tk.Entry(root, width=30)
        custID_entry.grid(row=3, column=1, padx=5, pady=5)

        def on_customer_id_button_click():
            user_input = custID_entry.get()
            # Validate customer ID
            try:
                customer_id = int(user_input)
                # Here you can use the customer_id for further processing
                custID_label.grid_remove()  # Remove the customer ID label and entry
                custID_entry.grid_remove()
                custID_entry_button.grid_remove()
                get_product_id(customer_id)  # Proceed to get the product ID
            except ValueError:
                print("Invalid Customer ID input")
                show_temporary_label("Invalid Input. Enter a valid Customer ID", error=True)

        custID_entry_button = tk.Button(root, text="Submit", command=on_customer_id_button_click)
        custID_entry_button.grid(row=3, column=2, padx=5, pady=5)

    def get_product_id(customer_id):
        nonlocal product_id  # Declare as nonlocal to modify the outer scope variable
        proID_label = tk.Label(root, text="Enter Product ID:")
        proID_label.grid(row=4, column=0, padx=5, pady=5)
        proID_entry = tk.Entry(root, width=30)
        proID_entry.grid(row=4, column=1, padx=5, pady=5)

        def on_product_id_button_click():
            user_input = proID_entry.get()
            # Validate product ID
            try:
                product_id = int(user_input)
                proID_label.grid_remove()  # Remove the product ID label and entry
                proID_entry.grid_remove()
                proID_entry_button.grid_remove()
                get_product_quantity(customer_id, product_id)  # Proceed to get the product quantity
                
            except ValueError:
                print("Invalid Product ID input")
                show_temporary_label("Invalid Input. Enter a valid Product ID", error=True)

        proID_entry_button = tk.Button(root, text="Submit", command=on_product_id_button_click)
        proID_entry_button.grid(row=4, column=2, padx=5, pady=5)
         

    def get_product_quantity(customer_id, product_id):
        quantity_label = tk.Label(root, text="Enter Product Quantity:")
        quantity_label.grid(row=5, column=0, padx=5, pady=5)
        quantity_entry = tk.Entry(root, width=30)
        quantity_entry.grid(row=5, column=1, padx=5, pady=5)

        def on_quantity_button_click():
            user_input = quantity_entry.get()
            # Validate quantity
            try:
                product_quantity = int(user_input)
                product_cost = get_product_price(product_quantity, product_id)
                update_product_order(product_quantity, product_id)
                # Insert order into customerorder table
                sql = f"INSERT INTO customerorder(CustomerID, ProductID, NumProduct, OrderTotal) VALUES ('{customer_id}', '{product_id}', '{product_quantity}', '{product_cost}')"
                cursor.execute(sql)
                connection.commit()
                print ("Order successfully created")
                quantity_label.grid_remove()  # Remove the quantity label and entry
                quantity_entry.grid_remove()
                quantity_entry_button.grid_remove()
                show_temporary_label("ORDER SUBMITTED", error = False)
                enable_buttons()
            except ValueError:
                print("Invalid Quantity input")
                show_temporary_label("Invalid Input. Enter a valid Product Quantity", error=True)

        quantity_entry_button = tk.Button(root, text="Submit", command=on_quantity_button_click)
        quantity_entry_button.grid(row=5, column=2, padx=5, pady=5)

    def update_product_order(product_quantity, product_id):
        query = f"select NumInStock from product where ProductID = {product_id}"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            in_stock = row[0]
        
        new_in_stock = in_stock - product_quantity

        sql = f"UPDATE product SET NumInStock = '{new_in_stock}' WHERE ProductID = '{product_id}'"
        cursor.execute(sql)

        query = f"select NumSales from product where ProductID = {product_id}"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            num_sales = row[0]
        
        new_num_sales = num_sales + product_quantity

        sql = f"UPDATE product SET NumSales = '{new_num_sales}' WHERE ProductID = '{product_id}'"
        cursor.execute(sql)

        connection.commit()

    def get_product_price(product_quantity, product_id):
        query = f"select Price from product where ProductID = {product_id}"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            individual_price = row[0]
        connection.commit()
        
        return(individual_price * product_quantity)

    get_customer_id()  # Start by getting the customer ID

def search_product():
    disable_buttons()
    def on_search_button_click():
        # Get the values from the input fields
        product_name = product_name_entry.get()
        product_id = product_id_entry.get()

        # Query product table
        if product_name == '':
            query = f"select * from product where ProductID = {product_id}"
        elif product_id == '':
            query = f"select * from product where ProductName = '{product_name}'"
        else:
            query = f"select * from product where ProductName = '{product_name}' and ProductID = {product_id}"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(f"Product ID: {row[0]}  |  Name: {row[1]}  |  Price: {row[2]}  |  Total Sales: {row[3]}  |  In Stock: {row[4]}")
        
        connection.commit()
        search_label.destroy()
        search_button.destroy()
        product_name_label.destroy()
        product_name_entry.destroy()
        product_id_label.destroy()
        product_id_entry.destroy()
        header = "Product ID | Product Name | Price | Total Sales | In Stock"
        display_search_results(rows, header)
        enable_buttons()

    search_label = tk.Label(root, text="Search Product:")
    search_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")

    # Input box for Product Name
    product_name_label = tk.Label(root, text="Product Name:")
    product_name_label.grid(row=7, column=1, padx=5, pady=5, sticky="e")
    product_name_entry = tk.Entry(root, width=30)
    product_name_entry.grid(row=7, column=2, padx=5, pady=5)

    # Input box for Product ID
    product_id_label = tk.Label(root, text="Product ID:")
    product_id_label.grid(row=7, column=3, padx=5, pady=5, sticky="e")
    product_id_entry = tk.Entry(root, width=30)
    product_id_entry.grid(row=7, column=4, padx=5, pady=5)

    # Search button
    search_button = tk.Button(root, text="Search", command=on_search_button_click)
    search_button.grid(row=7, column=5, padx=5, pady=5)

def search_customer():
    disable_buttons()
    def on_search_button_click():
        # Get the values from the input fields
        customer_id = customer_id_entry.get()
        customer_email = customer_email_entry.get()
        customer_name = customer_name_entry.get()

        # Query customer table
        query = f"select * from customer where CustomerID = {customer_id} or Email = '{customer_email}' or FullName = '{customer_name}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(f"Customer ID: {row[0]}  |  Email: {row[1]}  |  Name: {row[2]}")
        connection.commit()
        search_label.destroy()
        search_button.destroy()
        customer_email_label.destroy()
        customer_email_entry.destroy()
        customer_id_label.destroy()
        customer_id_entry.destroy()
        customer_name_label.destroy()
        customer_name_entry.destroy()
        header = "Customer ID | Email | Name |"
        display_search_results(rows, header)
        enable_buttons()

    search_label = tk.Label(root, text="Search Customer:")
    search_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")

    # Input box for Customer ID
    customer_id_label = tk.Label(root, text="Customer ID:")
    customer_id_label.grid(row=7, column=1, padx=5, pady=5, sticky="e")
    customer_id_entry = tk.Entry(root, width=30)
    customer_id_entry.grid(row=7, column=2, padx=5, pady=5)

    # Input box for Customer Email
    customer_email_label = tk.Label(root, text="Customer Email:")
    customer_email_label.grid(row=7, column=3, padx=5, pady=5, sticky="e")
    customer_email_entry = tk.Entry(root, width=30)
    customer_email_entry.grid(row=7, column=4, padx=5, pady=5)

    # Input box for Customer Name
    customer_name_label = tk.Label(root, text="Customer Name:")
    customer_name_label.grid(row=7, column=5, padx=5, pady=5, sticky="e")
    customer_name_entry = tk.Entry(root, width=30)
    customer_name_entry.grid(row=7, column=6, padx=5, pady=5)

    # Search button
    search_button = tk.Button(root, text="Search", command=on_search_button_click)
    search_button.grid(row=7, column=7, padx=5, pady=5)

def search_orders():
    disable_buttons()
    def on_search_button_click():
        # Get the values from the input fields
        order_date = order_date_entry.get()
        customer_id = customer_id_entry.get()
        product_id = product_id_entry.get()

        # Query customer table
        if order_date == '':
            query = f"select * from CustomerOrder where CustomerID = '{customer_id}' or ProductID = '{product_id}'"
        else:
            query = f"select * from CustomerOrder where DATE(OrderDate) = '{order_date}' or CustomerID = '{customer_id}' or ProductID = '{product_id}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(f"Order ID: {row[0]}  |  Date: {row[1]}  |  Customer ID: {row[2]}  |  Product ID: {row[3]}  |  Product Amount: {row[4]}  |  Order Total: ${row[5]}")
        connection.commit()
        search_label.destroy()
        search_button.destroy()
        order_date_label.destroy()
        order_date_entry.destroy()
        customer_id_label.destroy()
        customer_id_entry.destroy()
        product_id_label.destroy()
        product_id_entry.destroy()
        header = "Order ID | Date | Customer ID | Product ID | Product Amount | Order Total |"
        display_search_results(rows, header)
        enable_buttons()

    search_label = tk.Label(root, text="Search Orders:")
    search_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")

    # Input box for Order Date
    order_date_label = tk.Label(root, text="Order Date:")
    order_date_label.grid(row=7, column=1, padx=5, pady=5, sticky="e")
    order_date_entry = tk.Entry(root, width=30)
    order_date_entry.grid(row=7, column=2, padx=5, pady=5)

    # Input box for Customer ID
    customer_id_label = tk.Label(root, text="Customer ID:")
    customer_id_label.grid(row=7, column=3, padx=5, pady=5, sticky="e")
    customer_id_entry = tk.Entry(root, width=30)
    customer_id_entry.grid(row=7, column=4, padx=5, pady=5)

    # Input box for Product ID
    product_id_label = tk.Label(root, text="Product ID:")
    product_id_label.grid(row=7, column=5, padx=5, pady=5, sticky="e")
    product_id_entry = tk.Entry(root, width=30)
    product_id_entry.grid(row=7, column=6, padx=5, pady=5)

    # Search button
    search_button = tk.Button(root, text="Search", command=on_search_button_click)
    search_button.grid(row=7, column=7, padx=5, pady=5)





    
# Call this function to add the search orders sectio

# Exit Button
exit_button = tk.Button(root, text="Exit", command=root.destroy)

# Customer Button
customer_button = tk.Button(root, text="Add Customer", command=add_customer)
# Product Button
product_button = tk.Button(root, text="Add Product ", command=lambda: add_product_name("Product Name"))
# Order Button (placeholder function)
order_button = tk.Button(root, text="Add Order", command=lambda: order_pressed())

#SEARCH For Product Button
product_search = tk.Button(root, text="Product Search", command = search_product)
#SEARCH for Customer Button
customer_search= tk.Button(root, text="Customer Search", command =search_customer )
#SEARCH for Order Button
order_search= tk.Button(root, text= "Order Search", command = search_orders)




# Back button for the main screen
back_button_main = tk.Button(root, text="Back", command=lambda: back_to_menu())
back_button_main.grid(row=8, column=0, pady=20)
# Pack the buttons into the window
customer_button.grid(row=6, column=0, pady=10)
product_button.grid(row=6, column=1, pady=10)
order_button.grid(row=6, column=2, pady=10)
product_search.grid(row= 6, column=3, pady= 10)
customer_search.grid(row = 6, column=4, pady= 10)
order_search.grid(row = 6, column=5, pady= 10)
exit_button.grid(row=8, column=1, columnspan=3, pady=20)

# Start the Tkinter event loop
root.mainloop()