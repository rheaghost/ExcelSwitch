import tkinter as tk
from tkinter import filedialog
from pathlib import Path


def run(task):

    root = tk.Tk()
    root.withdraw()

    print("\nSelect an input Excel file.")

    input_file = filedialog.askopenfilename(
        title="Select input Excel file",
        filetypes=[
            ("Excel files", "*.xlsx *.xls"),
            ("All files", "*.*")
        ]
    )

    if not input_file:
        return {
            "success": False,
            "task_id": "024",
            "error": "No input file selected."
        }

    print("\nSelect output Excel file.")

    output_file = filedialog.asksaveasfilename(
        title="Select output Excel file",
        defaultextension=".xlsx",
        filetypes=[
            ("Excel files", "*.xlsx"),
            ("All files", "*.*")
        ]
    )

    root.destroy()

    if not output_file:
        return {
            "success": False,
            "task_id": "024",
            "input": input_file,
            "error": "No output file selected."
        }

    output_path = Path(output_file)

    print("\nFile selection complete.")
    print(f"Input : {input_file}")
    print(f"Output: {output_path}")

    
    if Path(input_file).resolve() == Path(output_file).resolve():
       return {
            "success": False,
            "task_id": "024",
            "input": input_file,
            "output": output_file,
            "error": "Input and output files must be different."
        }

    return {
        "success": True,
        "task_id": "024",
        "input": input_file,
        "output": str(output_path)
    }