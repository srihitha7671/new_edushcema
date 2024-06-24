import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Database connection function
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="India123#@",
        database="edu1"
    )

# Function to insert data into selected table
def insert_data():
    try:
        db = connect_db()
        cursor = db.cursor()

        table = table_selection.get()

        if table in TABLE_ID_COLUMN_MAP:
            id_column = TABLE_ID_COLUMN_MAP[table]
            columns = INSERT_FIELDS[table]
            values = tuple(entry_vars[table][column].get() for column in columns)

            query = f"INSERT INTO {table} ({', '.join(columns)}, deleted) VALUES ({', '.join(['%s'] * len(columns))}, 0)"
            cursor.execute(query, values)

            db.commit()
            messagebox.showinfo("Success", f"Data inserted into {table} successfully")
        else:
            messagebox.showwarning("Warning", "Please select a table to insert data.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

    finally:
        db.close()

# Function to update data in selected table
def update_data():
    try:
        db = connect_db()
        cursor = db.cursor()

        table = table_selection_update.get()
        update_id = update_id_entry.get()

        if table in TABLE_ID_COLUMN_MAP:
            id_column = TABLE_ID_COLUMN_MAP[table]
            columns = UPDATE_FIELDS[table]

            # Prepare the UPDATE query dynamically based on the selected table
            update_query = f"UPDATE {table} SET "
            update_query += ", ".join([f"{column} = %s" for column in columns])
            update_query += f" WHERE {id_column} = %s"

            # Prepare values for the query
            update_values = tuple(entry_vars_update[table][column].get() for column in columns) + (update_id,)

            cursor.execute(update_query, update_values)

            db.commit()
            messagebox.showinfo("Success", f"Data updated in {table} where ID = {update_id} successfully")
        else:
            messagebox.showwarning("Warning", "Please select a table to update data.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

    finally:
        db.close()

# Function to fetch data from the selected table with selected columns
def fetch_data(table_name, selected_columns):
    try:
        db = connect_db()
        cursor = db.cursor()

        # Create a comma-separated string of selected columns
        columns_str = ', '.join(selected_columns)

        # Construct the SQL query, excluding rows where deleted = 1
        query = f"SELECT {columns_str} FROM {table_name} WHERE deleted = 0"

        cursor.execute(query)
        rows = cursor.fetchall()

        db.close()

        return rows
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# Function to handle table selection change in Insert tab
def table_selected(*args):
    selected_table = table_selection.get()

    # Clear previous entry widgets
    for widget in insert_data_frame.winfo_children():
        widget.destroy()

    if selected_table in TABLE_ID_COLUMN_MAP:
        id_column = TABLE_ID_COLUMN_MAP[selected_table]
        columns = INSERT_FIELDS[selected_table]

        # Create entry widgets for each column
        for idx, column in enumerate(columns):
            tk.Label(insert_data_frame, text=f"{column}:").grid(row=idx, column=0, sticky='w')
            entry_var = tk.StringVar()
            entry_vars[selected_table][column] = entry_var
            tk.Entry(insert_data_frame, textvariable=entry_var).grid(row=idx, column=1)

        # Insert Button
        insert_button = tk.Button(insert_data_frame, text="Insert Data", command=insert_data)
        insert_button.grid(row=len(columns), columnspan=2, pady=10)

# Function to handle table selection change in Update tab
def table_selected_update(*args):
    selected_table = table_selection_update.get()

    # Clear previous entry widgets
    for widget in update_form_frame.winfo_children():
        widget.destroy()

    if selected_table in TABLE_ID_COLUMN_MAP:
        id_column = TABLE_ID_COLUMN_MAP[selected_table]
        columns = UPDATE_FIELDS[selected_table]

        # Create entry widgets for each column
        tk.Label(update_form_frame, text=f"{selected_table} ID:").grid(row=0, column=0, padx=10, pady=5)
        global update_id_entry
        update_id_entry = tk.Entry(update_form_frame)
        update_id_entry.grid(row=0, column=1, padx=10, pady=5)

        for idx, column in enumerate(columns):
            tk.Label(update_form_frame, text=f"New {column.replace('_', ' ').title()}:").grid(row=idx + 1, column=0, padx=10, pady=5)
            entry_var = tk.StringVar()
            entry_vars_update[selected_table][column] = entry_var
            tk.Entry(update_form_frame, textvariable=entry_var).grid(row=idx + 1, column=1, padx=10, pady=5)

        # Update Button
        update_button = tk.Button(update_form_frame, text="Update Data", command=update_data)
        update_button.grid(row=len(columns) + 1, columnspan=2, pady=10)

# Function to handle table selection change in Display tab
def table_selected_display(*args):
    selected_table = table_selection_display.get()

    # Clear previous widgets
    for widget in display_data_frame.winfo_children():
        widget.destroy()

    if selected_table:
        # Fetch columns for the selected table from database schema
        columns = fetch_table_columns(selected_table)

        if columns:
            # Create Checkbuttons for each column
            global display_columns_vars
            display_columns_vars = {}
            for idx, column in enumerate(columns):
                if column.lower() != "deleted":  # Exclude the 'deleted' column
                    var = tk.IntVar()
                    display_columns_vars[column] = var
                    chk = tk.Checkbutton(display_data_frame, text=column, variable=var)
                    chk.grid(row=idx, column=0, sticky='w')

            # Display Button
            display_button = tk.Button(display_data_frame, text="Display Selected Data", command=lambda: display_selected_data_in_tab(selected_table))
            display_button.grid(row=len(columns), columnspan=2, pady=10)

# Function to fetch columns of a table from the database schema
def fetch_table_columns(table_name):
    try:
        db = connect_db()
        cursor = db.cursor()

        # Query to fetch column names
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = [column[0] for column in cursor.fetchall()]

        db.close()

        return columns
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# Function to display selected data in a new tab
def display_selected_data_in_tab(selected_table):
    selected_columns = [column for column, var in display_columns_vars.items() if var.get() == 1]

    if selected_columns:
        data = fetch_data(selected_table, selected_columns)
        if data:
            # Create a new tab
            tab_name = f"{selected_table} - Data"
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text=tab_name)

            # Create a Treeview widget in the new tab
            display_treeview = ttk.Treeview(tab_frame, columns=selected_columns, show='headings')
            display_treeview.pack(padx=20, pady=20, fill='both', expand=True)

            # Configure columns for the treeview
            for col in selected_columns:
                display_treeview.heading(col, text=col)
                display_treeview.column(col, anchor=tk.CENTER, width=100)

            # Insert fetched data into treeview
            for row in data:
                display_treeview.insert('', 'end', values=row)
        else:
            messagebox.showinfo("Info", "No data to display.")
    else:
        messagebox.showwarning("Warning", "Please select at least one column to display.")

# Function to fetch row IDs of a table
def fetch_row_ids(table_name):
    try:
        db = connect_db()
        cursor = db.cursor()

        # Query to fetch row IDs where deleted = 0
        id_column = TABLE_ID_COLUMN_MAP[table_name]
        cursor.execute(f"SELECT {id_column} FROM {table_name} WHERE deleted = 0")
        row_ids = [row[0] for row in cursor.fetchall()]

        db.close()

        return row_ids
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# Function to populate row ID dropdown in Delete tab
def populate_row_id_dropdown(table_name):
    row_ids = fetch_row_ids(table_name)
    delete_id_combobox['values'] = row_ids
    delete_id_combobox.set('')

# Function to delete a row from the selected table
def delete_row():
    table_name = delete_table_combobox.get()
    row_id = delete_id_combobox.get()

    if table_name and row_id:
        try:
            db = connect_db()
            cursor = db.cursor()

            # Construct the SQL query to update the 'deleted' column
            id_column = TABLE_ID_COLUMN_MAP[table_name]
            query = f"UPDATE {table_name} SET deleted = 1 WHERE {id_column} = %s"
            cursor.execute(query, (row_id,))

            db.commit()
            db.close()

            messagebox.showinfo("Success", f"Row with ID {row_id} marked as deleted.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
    else:
        messagebox.showwarning("Warning", "Please select both table name and ID.")

# Main application window
root = tk.Tk()
root.title("Database Management System")

# Notebook for tab management
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, fill='both', expand=True)

# Define global variables
TABLE_ID_COLUMN_MAP = {
    "Courses": "course_id",
    "Instructors": "instructor_id",
    "Students": "student_id",
    "Enrolments": "enrolment_id",
    "Assessments": "assessment_id",
    "Grades": "grade_id"
}

INSERT_FIELDS = {
    "Courses": ["course_name", "course_description", "course_start_date", "course_end_date"],
    "Instructors": ["instructor_name", "instructor_email", "instructor_bio"],
    "Students": ["student_name", "student_email", "student_date_of_birth"],
    "Enrolments": ["student_id", "course_id", "enrolment_date", "completion_status"],
    "Assessments": ["course_id", "assessment_name", "assessment_date", "max_score"],
    "Grades": ["assessment_id", "student_id", "score"]
}

UPDATE_FIELDS = {
    "Courses": ["course_name", "course_description", "course_start_date", "course_end_date"],
    "Instructors": ["instructor_name", "instructor_email", "instructor_bio"],
    "Students": ["student_name", "student_email", "student_date_of_birth"],
    "Enrolments": ["student_id", "course_id", "enrolment_date", "completion_status"],
    "Assessments": ["course_id", "assessment_name", "assessment_date", "max_score"],
    "Grades": ["assessment_id", "student_id", "score"]
}

entry_vars = {table: {field: tk.StringVar() for field in fields} for table, fields in INSERT_FIELDS.items()}
entry_vars_update = {table: {field: tk.StringVar() for field in fields} for table, fields in UPDATE_FIELDS.items()}

# Insert tab
tab_insert = ttk.Frame(notebook)
notebook.add(tab_insert, text="Insert")

# Widgets for Insert tab
table_selection_label = tk.Label(tab_insert, text="Select Table:")
table_selection_label.grid(row=0, column=0, padx=10, pady=5)

global table_selection
table_selection = ttk.Combobox(tab_insert, values=list(TABLE_ID_COLUMN_MAP.keys()), state="readonly")
table_selection.grid(row=0, column=1, padx=10, pady=5)
table_selection.bind("<<ComboboxSelected>>", table_selected)

insert_data_frame = ttk.Frame(tab_insert)
insert_data_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Update tab
tab_update = ttk.Frame(notebook)
notebook.add(tab_update, text="Update")

# Widgets for Update tab
table_selection_update_label = tk.Label(tab_update, text="Select Table:")
table_selection_update_label.grid(row=0, column=0, padx=10, pady=5)

global table_selection_update
table_selection_update = ttk.Combobox(tab_update, values=list(UPDATE_FIELDS.keys()), state="readonly")
table_selection_update.grid(row=0, column=1, padx=10, pady=5)
table_selection_update.bind("<<ComboboxSelected>>", table_selected_update)

update_form_frame = ttk.Frame(tab_update)
update_form_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Display tab
tab_display = ttk.Frame(notebook)
notebook.add(tab_display, text="Display")

# Widgets for Display tab
table_selection_display_label = tk.Label(tab_display, text="Select Table:")
table_selection_display_label.grid(row=0, column=0, padx=10, pady=5)

global table_selection_display
table_selection_display = ttk.Combobox(tab_display, values=list(TABLE_ID_COLUMN_MAP.keys()), state="readonly")
table_selection_display.grid(row=0, column=1, padx=10, pady=5)
table_selection_display.bind("<<ComboboxSelected>>", table_selected_display)

display_data_frame = ttk.Frame(tab_display)
display_data_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Delete tab
tab_delete = ttk.Frame(notebook)
notebook.add(tab_delete, text="Delete")

# Widgets for Delete tab
delete_table_label = tk.Label(tab_delete, text="Select Table:")
delete_table_label.grid(row=0, column=0, padx=10, pady=5)

global delete_table_combobox
delete_table_combobox = ttk.Combobox(tab_delete, values=list(TABLE_ID_COLUMN_MAP.keys()), state="readonly")
delete_table_combobox.grid(row=0, column=1, padx=10, pady=5)
delete_table_combobox.bind("<<ComboboxSelected>>", lambda event: populate_row_id_dropdown(delete_table_combobox.get()))

delete_id_label = tk.Label(tab_delete, text="Select ID:")
delete_id_label.grid(row=1, column=0, padx=10, pady=5)

global delete_id_combobox
delete_id_combobox = ttk.Combobox(tab_delete, state="readonly")
delete_id_combobox.grid(row=1, column=1, padx=10, pady=5)

delete_button = tk.Button(tab_delete, text="Delete Row", command=delete_row)
delete_button.grid(row=2, columnspan=2, pady=10)

root.mainloop()