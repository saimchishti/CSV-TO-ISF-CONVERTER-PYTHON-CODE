import pandas as pd
import tkinter as tk
from tkinter import filedialog
import re

# Function to clean the dataset by removing special symbols, white spaces, and unnecessary characters
def clean_dataset(df):
    # Define a function to remove special symbols, except underscore, and spaces
    def clean_string(s):
        return re.sub(r'[^\w]', '', s)  # Remove all special characters and spaces except underscore

    # Apply the cleaning function to all data entries
    df = df.applymap(lambda x: clean_string(str(x)) if isinstance(x, str) else x)
    # Apply the cleaning function to column names
    df.columns = [clean_string(col) for col in df.columns]

    return df

# Function to round off all decimal values to integers in the DataFrame
def round_decimal_values(df):
    return df.applymap(lambda x: round(x) if isinstance(x, (float, int)) else x)

# Function to convert CSV to ISF format
def csv_to_isf(csv_file_path, isf_file_path):
    # Read the CSV file into a DataFrame with header
    df = pd.read_csv(csv_file_path)

    # Clean the entire DataFrame and column names by removing spaces and special symbols
    df = clean_dataset(df)

    # Round off all decimal values to integers
    df = round_decimal_values(df)

    # Extract attributes and decision class
    attributes = df.columns[:-1]  # All columns except the last one are attributes
    decision_class = df.columns[-1]  # The last column is the decision class

    # Determine unique values for each attribute
    unique_values = {}
    for attr in attributes:
        unique_values[attr] = sorted(df[attr].unique())
    unique_values[decision_class] = sorted(df[decision_class].unique())

    # Open the ISF file for writing
    with open(isf_file_path, 'w') as isf_file:
        # Write the attributes section
        isf_file.write("**ATTRIBUTES\n")
        for attr in attributes:
            isf_file.write(f" + {attr}: [{', '.join(map(str, unique_values[attr]))}]\n")
        isf_file.write(f" + {decision_class}: [{', '.join(map(str, unique_values[decision_class]))}]\n")
        isf_file.write(f" + decision: {decision_class}\n")

        # Write the preferences section
        isf_file.write("**PREFERENCES\n")
        for attr in attributes:
            isf_file.write(f" {attr} : gain\n")
        isf_file.write(f" {decision_class} : gain\n")

        # Write the examples section
        isf_file.write("**EXAMPLES\n")
        for index, row in df.iterrows():
            line = " ".join(str(value) for value in row)
            isf_file.write(line + "\n")

        # End marker
        isf_file.write("**END\n")

def select_file_and_convert():
    # Initialize Tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    # Open file dialog to select CSV file
    csv_file_path = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV files", "*.csv")]
    )

    if not csv_file_path:
        print("No file selected.")
        return

    # Prompt user for ISF file path
    isf_file_path = filedialog.asksaveasfilename(
        title="Save ISF file as",
        defaultextension=".isf",
        filetypes=[("ISF files", "*.isf")]
    )

    if not isf_file_path:
        print("No file selected.")
        return

    # Convert the selected CSV file to ISF format
    csv_to_isf(csv_file_path, isf_file_path)
    print(f"Conversion complete: {csv_file_path} -> {isf_file_path}")

# Run the file selection and conversion
select_file_and_convert()
