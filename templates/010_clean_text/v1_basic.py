import pandas as pd


def run(task):

    input_file = task["input"]
    output_file = task["output"]
    columns = task["columns"]

    df = pd.read_excel(input_file)

    for column in columns:

        if column not in df.columns:
            raise ValueError(
                f"Column '{column}' does not exist."
            )

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .str.replace(
                r"\s+",
                " ",
                regex=True
            )
        )

    df.to_excel(
        output_file,
        index=False
    )

    print("\nText cleaning complete.")
    print(f"Columns cleaned: {columns}")
    print(f"Output: {output_file}")

    return {
        "success": True,
        "task_id": "010",
        "input": input_file,
        "output": output_file,
        "cleaned_columns": columns
    }