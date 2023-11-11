
from tkinter import *
from tkinter import ttk
import datetime as dt
from tkinter import messagebox
import sqlite3
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Database class for expense records
class ExpenseDatabase:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS expense_record (expense_name text, price float, purchase_date date, category text, subcategory text, payment_mode text, description text)")
        self.conn.commit()

    def fetchRecord(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def insertRecord(self, expense_name, price, purchase_date, category, subcategory,payment_mode, description):
        self.cur.execute("INSERT INTO expense_record VALUES (?, ?, ?, ?, ?, ?, ?)",
                         (expense_name, price, purchase_date, category, subcategory, payment_mode, description))
        self.conn.commit()

    def removeRecord(self, rwid):
        self.cur.execute("DELETE FROM expense_record WHERE rowid=?", (rwid,))
        self.conn.commit()

    def updateRecord(self, expense_name, price, purchase_date, category, subcategory, payment_mode, description, rid):
        self.cur.execute("UPDATE expense_record SET expense_name = ?, price = ?, purchase_date = ?, category = ?, subcategory = ?, payment_mode = ?, description = ? WHERE rowid = ?",
                         (expense_name, price, purchase_date, category, subcategory, payment_mode, description, rid))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

# Database class for categories and subcategories
class CategoryDatabase:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS category (category_name text, subcategory_name text)")
        self.conn.commit()

    def fetchCategories(self):
        self.cur.execute("SELECT category_name, subcategory_name FROM category")
        rows = self.cur.fetchall()
        return rows

    def insertCategory(self, category_name, subcategory_name):
        self.cur.execute("INSERT INTO category (category_name, subcategory_name) VALUES (?, ?)", (category_name, subcategory_name))
        self.conn.commit()
        refreshData(self)

    def __del__(self):
        self.conn.close()

# global variables
count = 0
selected_rowid = 0

# functions

def addDescription():
    description = askstring("Add Description", "Enter Description:")
    if description:
        description_var.set(description)

def saveRecord():
    global expense_db
    expense_db.insertRecord(expense_name.get(), price.get(), transaction_date.get(), category_var.get(), subcategory_var.get(), payment_mode_var.get(), description_var.get())

def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %b %Y}')

def clearEntries():
    expense_name.delete(0, 'end')
    price.delete(0, 'end')
    transaction_date.delete(0, 'end')
    category_var.set('')  
    subcategory_var.set('') 
    payment_mode_var.set('')
    description_var.set('')

def fetch_records():
    f = expense_db.fetchRecord('SELECT rowid, * FROM expense_record')
    global count
    for rec in f:
        tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7]))
        count += 1
    tv.after(400, refreshData)

def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')

    try:
        selected_rowid = val[0]
        d = val[3]
        expense_name_var.set(val[1])
        price_var.set(val[2])
        dopvar.set(str(d))
        category_var.set(val[4])
        subcategory_var.set(val[5])
        payment_mode_var.set(val[6])
        description_var.set(val[7])
    except Exception as ep:
        pass

def update_record():
    global selected_rowid

    selected = tv.focus()
    # Update record
    try:
        expense_db.updateRecord(expense_name_var.get(), price_var.get(), dopvar.get(), category_var.get(), subcategory_var.get(), payment_mode_var.get(), description_var.get(), selected_rowid)
        tv.item(selected, text="", values=(selected_rowid, expense_name_var.get(), price_var.get(), dopvar.get(), category_var.get(), subcategory_var.get(), payment_mode_var.get(), description_var.get()))
    except Exception as ep:
        messagebox.showerror('Error', ep)

    # Clear entry boxes
    clearEntries()
    tv.after(400, refreshData)

def deleteRow():
    global selected_rowid
    if selected_rowid:
        expense_db.removeRecord(selected_rowid)
        refreshData()
    else:
        messagebox.showinfo('Info', 'Please select a record to delete.')

def totalBalance():   ##  Total Expense
    f = expense_db.fetchRecord("SELECT sum(price) FROM expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo('Current Balance:', f"Total Expense: ₹ {j}")

def refreshData():
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()

# New function to add a category via a popup dialog
def addCategory():
    category_name = askstring("Add Category", "Enter Category Name:")
    if category_name:
        subcategory_name = askstring("Add Subcategory", "Enter Subcategory Name:")
        if subcategory_name:
            category_db.insertCategory(category_name, subcategory_name)

# New function to add a subcategory via a popup dialog
def addSubcategory():
    category_name = askstring("Add Subcategory", "Enter Category Name:")
    if category_name:
        subcategory_name = askstring("Add Subcategory", "Enter Subcategory Name:")
        if subcategory_name:
            category_db.insertCategory(category_name, subcategory_name)

# Function to populate category dropdown menu
def populate_category_dropdown():
    category_list = category_db.fetchCategories()
    categories = set()
    for row in category_list:
        category_name, subcategory_name = row
        categories.add(category_name)
    category_var.set('')
    category_dropdown['menu'].delete(0, 'end')
    category_dropdown['menu'].add_command(label='', command=lambda: category_var.set(''))
    for category in categories:
        category_dropdown['menu'].add_command(label=category, command=lambda c=category: category_var.set(c))

def populate_subcategory_dropdown(selected_category):
    if selected_category:
        subcategory_dropdown['menu'].delete(0, 'end')
        subcategory_dropdown['menu'].add_command(label='', command=lambda: subcategory_var.set(''))
        subcategories = set()
        for row in category_db.fetchCategories():
            category_name, subcategory_name = row
            if category_name == selected_category:
                subcategories.add(subcategory_name)
        for subcategory in subcategories:
            subcategory_dropdown['menu'].add_command(label=subcategory, command=lambda sc=subcategory: subcategory_var.set(sc))
    else:
        subcategory_dropdown['menu'].delete(0, 'end')
        subcategory_var.set('')


def analyze_expenses():
    messagebox.showinfo('Information', ' Statistics Under Development. \n Work Under Process. \n Visit Later for Statistics.')

# --------------------------------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX--------------------------------------
# ------------------------------------------------------              _Statistics Under Development Process_               -----------------------------------------------------------------
    # # Fetch expense data from the database
    # query1 = "SELECT strftime('%Y-%m-%d', purchase_date) as date, sum(price) as total_price FROM expense_record GROUP BY date"
    # expense_data = expense_db.fetchRecord(query1)

    # # Convert data to a DataFrame for easier manipulation
    # df = pd.DataFrame(expense_data, columns=["Date", "Total Price"])

    # # Drop rows with missing values in the date column
    # df = df.dropna(subset=['Date'])

    # # Convert the 'Date' column to datetime
    # df['Date'] = pd.to_datetime(df['Date'])

    # # Analysis type selection using a Combobox
    # analysis_types = ["Daily", "Weekly", "Monthly", "Yearly"]
    # selected_analysis_type = ttk.Combobox(ws, values=analysis_types)
    # selected_analysis_type.set("Daily")  # Set a default value

    # # Prompt user to select analysis type
    # user_choice = askstring("Analysis Type", "Select Analysis Type:", initialvalue=selected_analysis_type.get())

    # if user_choice in analysis_types:
    #     selected_analysis_type.set(user_choice)

    #     # Perform analysis based on the selected type
    #     if user_choice.lower() == 'daily':
    #         df_resampled = df.set_index('Date')
    #     elif user_choice.lower() == 'weekly':
    #         df_resampled = df.resample('W-Mon', on='Date').sum()
    #     elif user_choice.lower() == 'monthly':
    #         df_resampled = df.resample('M', on='Date').sum()
    #     elif user_choice.lower() == 'yearly':
    #         df_resampled = df.resample('Y', on='Date').sum()

    #     # Check if the DataFrame is not empty before plotting
    #     if not df_resampled.empty:
    #         # Highlight max expenses
    #         max_expense = df_resampled['Total Price'].max()
    #         max_expense_date = df_resampled[df_resampled['Total Price'] == max_expense].index[0]

    #         # Reset the index for plotting
    #         df_resampled = df_resampled.reset_index()

    #         # Plotting the graph
    #         fig, ax = plt.subplots()
    #         df_resampled.plot(kind='bar', x='Date', y='Total Price', ax=ax)
    #         ax.set_title(f"Expense Analysis ({user_choice})")
    #         ax.set_xlabel("Date")
    #         ax.set_ylabel("Total Expense")
    #         plt.xticks(rotation=45)

    #         # Highlight max expenses
    #         ax.annotate(f'Max Expense: {max_expense:.2f}', xy=(max_expense_date, max_expense),
    #                     xytext=(max_expense_date, max_expense * 1.2),
    #                     arrowprops=dict(facecolor='red', arrowstyle='->'))

    #         # Display the graph in a new window
    #         graph_window = Toplevel(ws)
    #         canvas = FigureCanvasTkAgg(fig, master=graph_window)
    #         canvas.draw()
    #         canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    #         toolbar = NavigationToolbar2Tk(canvas, graph_window)
    #         toolbar.update()
    #         canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    #     else:
    #         messagebox.showinfo('Info', f'No data available for the selected analysis type ({user_choice}).')
    # else:
    #     messagebox.showinfo('Info', 'Invalid analysis type selected.')

# -----------------------------------------------------------------------------------------------XXXXXXXXXXXXXXXXXXXXXXXX-------------------------------------------------------------------
# --------------------------------------------------------XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX--------------------------------------


# create tkinter object
ws = Tk()
ws.title('Personal Expense Management App')

# List of payment modes
PaymentModes = ["Online", "Cash", "Credit", "Other"] 

# variables
f = ('Times new roman', 14)
expense_name_var = StringVar()
price_var = DoubleVar()
dopvar = StringVar()
category_var = StringVar()
subcategory_var = StringVar()
description_var = StringVar()

# Payment mode variable
payment_mode_var = StringVar()
payment_mode_var.set(PaymentModes[0])  # Initialize with the first payment mode 

# Frame widget
f2 = Frame(ws, bg='#EBE3D5')
f2.pack()

f1 = Frame(
    ws,
    padx=15,
    pady=15,
)
f1.pack(expand=True, fill=BOTH)

# Create an ImageTk.PhotoImage from an image file
image = Image.open("C:\\Users\\kumar\\Pictures\\expenses.png")  # Replace with the actual image file path
image = ImageTk.PhotoImage(image)

# Create a label to display the image
image_label = Label(f1, image=image)
image_label.grid(row=0, column=5, rowspan=7, padx=(20, 10))

# Label widget
Label(f1, text='Expense Name', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='Price', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='Date', font=f).grid(row=2, column=0, sticky=W)
Label(f1, text='Category', font=f).grid(row=3, column=0, sticky=W)
Label(f1, text='Subcategory', font=f).grid(row=4, column=0, sticky=W)
Label(f1, text='Payment Mode', font=f).grid(row=5, column=0, sticky=W)
Label(f1, text='Description', font=f).grid(row=6, column=0, sticky=W)

# Entry widgets
expense_name = Entry(f1, font=f, textvariable=expense_name_var)
price = Entry(f1, font=f, textvariable=price_var)
transaction_date = Entry(f1, font=f, textvariable=dopvar)
category_entry = Entry(f1, font=f, textvariable=category_var)
subcategory_entry = Entry(f1, font=f, textvariable=subcategory_var)
payment_mode_entry = OptionMenu(f1, payment_mode_var, *PaymentModes)
description_entry = Entry(f1, font=f, textvariable=description_var)

# Entry grid placement
expense_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
price.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))
category_entry.grid(row=3, column=1, sticky=EW, padx=(10, 0))
subcategory_entry.grid(row=4, column=1, sticky=EW, padx=(10, 0))
payment_mode_entry.grid(row=5, column=1, sticky=EW, padx=(10, 0))
description_entry.grid(row=6,column=1, sticky=EW, padx=(15, 1))

## Action buttons
cur_date = Button(
    f1,
    text='Current Date',
    font=f,
    bg='#E9FFC2',
    command=setDate,
    width=15
)

submit_btn = Button(
    f1,
    text='Save Record',
    font=f,
    command=saveRecord,
    bg='#00A9FF',
)

clr_btn = Button(
    f1,
    text='Clear Entry',
    font=f,
    command=clearEntries,
    bg='#89CFF3',
)

quit_btn = Button(
    f1,
    text='Exit',
    font=f,
    command=lambda: ws.destroy(),
    bg='#A0E9FF',
)

total_bal = Button(
    f1,
    text='Total Expenses',
    font=f,
    bg='#00A9FF',
    command=totalBalance
)

update_btn = Button(
    f1,
    text='Update',
    bg='#89CFF3',
    command=update_record,
    font=f
)

del_btn = Button(
    f1,
    text='Delete',
    bg='#A0E9FF',
    command=deleteRow,
    font=f
)

add_category_btn = Button(
    f1,
    text='Add Category',
    font=f,
    command=addCategory,
    bg='#CDF5FD',
)

add_subcategory_btn = Button(
    f1,
    text='Add Subcategory',
    font=f,
    command=addSubcategory,
    bg='#CDF5FD',
)

add_description_btn = Button(
    f1,
    text='Add Description',
    font=f,
    command=addDescription,
    bg='#CDF5FD',
)

stats_btn = Button(
    f1,
    text='Statistics',
    font=f,
    command=analyze_expenses,
    bg='#FECB52',
)


# Grid placement
cur_date.grid(row=5, column=2, sticky=EW, padx=(10, 0))
submit_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=3, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=1, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=3, column=3, sticky=EW, padx=(10, 0))
stats_btn.grid(row=6, column=2, sticky=EW, padx=(10, 0))


# Treeview widget
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4, 5, 6, 7, 8), show='headings', height=15)
tv.pack(side="left")


# Add heading to treeview
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.column(5, anchor=CENTER)
tv.column(6, anchor=CENTER)
tv.column(7, anchor=CENTER)
tv.column(8, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Expense Name")
tv.heading(3, text="Price")
tv.heading(4, text="Date")
tv.heading(5, text="Category")
tv.heading(6, text="Subcategory")
tv.heading(7, text="Payment Mode")
tv.heading(8, text="Description")


# Binding treeview
tv.bind("<ButtonRelease-1>", select_record)


# Style for treeview
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")


# Vertical scrollbar
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)


# Grid placement for the add category button
add_category_btn.grid(row=4, column=2, sticky=EW, padx=(10, 0))


# Grid placement for the add subcategory button
add_subcategory_btn.grid(row=4, column=3, sticky=EW, padx=(10, 0))


# Create a Database object for expense records
expense_db = ExpenseDatabase(db='Personal_Expense.db')


# Create a Database object for categories and subcategories
category_db = CategoryDatabase(db='Category_Expense.db')


# Create category and subcategory dropdown menus
category_label = Label(f1, text='Category', font=f)
category_label.grid(row=3, column=0, sticky=W)


category_var = StringVar()
category_dropdown = OptionMenu(f1, category_var, '')
category_dropdown.grid(row=3, column=1, sticky=EW)
category_var.trace('w', lambda *args: populate_subcategory_dropdown(category_var.get()))


subcategory_label = Label(f1, text='Subcategory', font=f)
subcategory_label.grid(row=4, column=0, sticky=W)


subcategory_var = StringVar()
subcategory_dropdown = OptionMenu(f1, subcategory_var, '')
subcategory_dropdown.grid(row=4, column=1, sticky=EW)


# Populate category dropdown
populate_category_dropdown()


# Calling function
fetch_records()


# Infinite loop
ws.mainloop()

