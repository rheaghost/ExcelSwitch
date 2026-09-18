import pandas as pd


def run(task):

    input_file = task["input"]
    output_file = task["output"]

    df = pd.read_excel(input_file)

    missing_before = int(df.isna().sum().sum())

    # Fill numeric columns with 0
    numeric_columns = df.select_dtypes(include="number").columns
    df[numeric_columns] = df[numeric_columns].fillna(0)

    # Fill text columns with an empty string
    text_columns = df.select_dtypes(include="object").columns
    df[text_columns] = df[text_columns].fillna("")

    missing_after = int(df.isna().sum().sum())

    df.to_excel(output_file, index=False)

    print("\nMissing-value processing complete.")
    print(f"Missing values before: {missing_before}")
    print(f"Missing values after : {missing_after}")
    print(f"Output file: {output_file}")

    return {
        "success": True,
        "task_id": "003",
        "input": input_file,
        "output": output_file,
        "missing_before": missing_before,
        "missing_after": missing_after
    }