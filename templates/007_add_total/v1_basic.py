import pandas as pd


def run(task):

    input_file = task["input"]
    output_file = task["output"]

    df = pd.read_excel(input_file)

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    total_row = {}

    for column in df.columns:

        if column in numeric_columns:
            total_row[column] = df[column].sum()
        else:
            total_row[column] = ""

    df.loc[len(df)] = total_row

    df.to_excel(
        output_file,
        index=False
    )

    print("\nTotal row added.")
    print(f"Numeric columns: {list(numeric_columns)}")
    print(f"Output: {output_file}")

    return {
        "success": True,
        "task_id": "007",
        "input": input_file,
        "output": output_file,
        "numeric_columns": list(numeric_columns)
    }