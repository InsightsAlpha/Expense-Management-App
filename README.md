# Expense Management App

The Expense Management App is a user-friendly and versatile tool designed to simplify and streamline the process of tracking personal expenses. Developed using Python and Tkinter, this application empowers users to record, manage, and analyze their financial transactions effortlessly. Whether you are keen on gaining insights into your spending patterns or looking for a convenient way to organize your expenses, this app is tailored to meet your needs.

## Table of Contents
1. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
2. [Features](#features)
3. [How to Use](#how-to-use)
4. [Database Structure](#database-structure)
5. [User Interface](#user-interface)
6. [Contributing](#contributing)
7. [License](#license)
8. [Acknowledgments](#acknowledgments)
9. [Desktop App File Download ](DeskApp)

## Getting Started

### Prerequisites

Before you begin, ensure you have Python installed on your machine. The application uses several Python libraries, which you can install using the following command:

```bash
pip install pillow matplotlib pandas
```

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/expense-management-app.git
```

2. Navigate to the project directory:

```bash
cd expense-management-app
```

3. Run the application:

```bash
python expense_management_app.py
```

## Features

- **Expense Recording:** Record essential details of your expenses, including name, price, date, category, subcategory, payment mode, and description.

- **Current Date Button:** Quickly populate the date field with the current date by clicking the "Current Date" button.

- **Save Record:** Save entered expense records to a SQLite database for organized storage.

- **Clear Entry Button:** Clear all input fields to facilitate the entry of new expense records.

- **Total Expenses Button:** View the total sum of all recorded expenses.

- **Update and Delete:** Modify or delete existing expense records with the "Update" and "Delete" buttons.

- **Add Category and Subcategory:** Expand and customize expense categories and subcategories.

- **Add Description Button:** Add descriptive notes to provide context to your expenses.

- **Statistics (Under Development):** Future functionality for generating and visualizing expense statistics based on different time intervals.

## How to Use

1. Run the application using `python expense_management_app.py`.
2. Enter expense details in the provided fields.
3. Use the action buttons to save, update, or delete expense records.
4. Explore additional features such as adding categories, subcategories, and descriptions.
5. Utilize the "Total Expenses" button to view the sum of all recorded expenses.

## Database Structure

The application utilizes two SQLite databases:

- **Personal_Expense.db:** Stores expense records.
- **Category_Expense.db:** Stores categories and subcategories.

The tables within these databases maintain a structured and organized storage of data.

## User Interface

The graphical user interface (GUI) provides an intuitive and user-friendly experience. It includes entry fields, buttons, and interactive widgets, all designed to simplify the expense tracking process. Dropdown menus for categories and subcategories enhance the accuracy of data entry.

## Contributing

We welcome contributions! Feel free to open issues, submit pull requests, or offer suggestions to improve the application.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to the open-source community for their contributions and inspiration. Together, we can build tools that make personal finance management accessible and effective.
