import pandas as pd


def run(task):

    input_file = task["input"]
    output_file = task["output"]
    rename_map = task["rename_map"]

    df = pd.read_excel(input_file)

    missing_columns = [
        column
        for column in rename_map
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Columns not found: {missing_columns}"
        )

    df = df.rename(
        columns=rename_map
    )

    df.to_excel(
        output_file,
        index=False
    )

    print("\nColumns renamed.")

    for old, new in rename_map.items():
        print(f"  {old} -> {new}")

    print(f"Output: {output_file}")

    return {
        "success": True,
        "task_id": "008",
        "input": input_file,
        "output": output_file,
        "renamed": rename_map
    }