import pandas as pd


def run(task):

    input_file = task["input"]
    output_file = task["output"]

    column = task["column"]
    value = task["value"]

    df = pd.read_excel(input_file)

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    filtered = df[
        df[column]
        .astype(str)
        .str.contains(
            str(value),
            case=False,
            na=False
        )
    ]

    filtered.to_excel(
        output_file,
        index=False
    )

    print("\nFiltering complete.")
    print(f"Column       : {column}")
    print(f"Search value : {value}")
    print(f"Rows before  : {len(df)}")
    print(f"Rows after   : {len(filtered)}")
    print(f"Output       : {output_file}")

    return {
        "success": True,
        "task_id": "009",
        "input": input_file,
        "output": output_file,
        "column": column,
        "condition": value,
        "rows_before": len(df),
        "rows_after": len(filtered)
    }