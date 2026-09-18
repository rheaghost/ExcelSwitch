import pandas as pd


def run(task):
    input_file = task["input"]

    df = pd.read_excel(input_file)

    result = {
        "success": True,
        "file": input_file,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns)
    }

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nFile information:")
    print(f"Rows: {result['rows']}")
    print(f"Columns: {result['columns']}")
    print(f"Columns names: {result['column_names']}")

    return result