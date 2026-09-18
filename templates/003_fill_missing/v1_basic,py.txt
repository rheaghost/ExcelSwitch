import pandas as pd


def run(task):

    input_file_1 = task["input_1"]
    input_file_2 = task["input_2"]
    output_file = task["output"]

    df1 = pd.read_excel(input_file_1)
    df2 = pd.read_excel(input_file_2)

    rows_before = len(df1) + len(df2)

    combined = pd.concat(
        [df1, df2],
        ignore_index=True
    )

    combined.to_excel(output_file, index=False)

    print("\nExcel files combined.")
    print(f"File 1 rows: {len(df1)}")
    print(f"File 2 rows: {len(df2)}")
    print(f"Combined rows: {len(combined)}")
    print(f"Output: {output_file}")

    return {
        "success": True,
        "task_id": "004",
        "input_1": input_file_1,
        "input_2": input_file_2,
        "output": output_file,
        "rows_before": rows_before,
        "rows_after": len(combined)
    }