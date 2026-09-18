import pandas as pd


def run(task):

    input_file_1 = task["input_1"]
    input_file_2 = task["input_2"]
    output_file = task["output"]

    key = task["key"]

    df1 = pd.read_excel(input_file_1)
    df2 = pd.read_excel(input_file_2)

    if key not in df1.columns:
        raise ValueError(
            f"Key column '{key}' does not exist in first file."
        )

    if key not in df2.columns:
        raise ValueError(
            f"Key column '{key}' does not exist in second file."
        )

    merged = pd.merge(
        df1,
        df2,
        on=key,
        how="left"
    )

    merged.to_excel(
        output_file,
        index=False
    )

    print("\nExcel merge complete.")
    print(f"Key column : {key}")
    print(f"First file : {len(df1)} rows")
    print(f"Second file: {len(df2)} rows")
    print(f"Result     : {len(merged)} rows")
    print(f"Output     : {output_file}")

    return {
        "success": True,
        "task_id": "011",
        "input_1": input_file_1,
        "input_2": input_file_2,
        "output": output_file,
        "key": key,
        "rows_first_file": len(df1),
        "rows_second_file": len(df2),
        "rows_result": len(merged)
    }