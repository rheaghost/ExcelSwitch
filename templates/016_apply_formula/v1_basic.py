# https://chatgpt.com/c/6a92cd47-160c-83e8-9b00-399399aaf71f
import pandas as pd


def run(task):

    input_file = task["input"]
    output_file = task["output"]

    column_1 = task["column_1"]
    column_2 = task["column_2"]
    new_column = task["new_column"]

    df = pd.read_excel(input_file)

    for column in [column_1, column_2]:
        if column not in df.columns:
            raise ValueError(
                f"Column '{column}' does not exist."
            )

    df[new_column] = df[column_1] * df[column_2]

    df.to_excel(
        output_file,
        index=False
    )

    print("\nFormula applied.")
    print(f"Column 1 : {column_1}")
    print(f"Column 2 : {column_2}")
    print(f"New column: {new_column}")
    print(f"Rows     : {len(df)}")
    print(f"Output   : {output_file}")

    return {
        "success": True,
        "task_id": "016",
        "input": input_file,
        "output": output_file,
        "column_1": column_1,
        "column_2": column_2,
        "new_column": new_column,
        "rows": len(df)
    }