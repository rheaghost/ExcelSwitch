import pandas as pd


def run(task):

    input_file = task["input"]
    output_file = task["output"]
    column = task["column"]

    df = pd.read_excel(input_file)

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    original_nonempty = df[column].notna().sum()

    df[column] = pd.to_datetime(
        df[column],
        dayfirst=True,
        errors="coerce"
    )

    converted_nonempty = df[column].notna().sum()

    df[column] = df[column].dt.strftime("%Y-%m-%d")

    df.to_excel(
        output_file,
        index=False
    )

    print("\nDate conversion complete.")
    print(f"Column: {column}")
    print(f"Recognized dates: {converted_nonempty}")
    print(f"Output: {output_file}")

    return {
        "success": True,
        "task_id": "006",
        "input": input_file,
        "output": output_file,
        "column": column,
        "recognized_dates": int(converted_nonempty),
        "original_nonempty": int(original_nonempty)
    }