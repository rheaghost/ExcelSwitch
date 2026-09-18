import pandas as pd


def run(task):

    input_file = task["input"]
    output_file = task["output"]

    id_columns = task["id_columns"]
    value_columns = task["value_columns"]

    df = pd.read_excel(input_file)

    # Validate ID columns
    for column in id_columns:
        if column not in df.columns:
            raise ValueError(
                f"ID column '{column}' does not exist."
            )

    # Validate value columns
    for column in value_columns:
        if column not in df.columns:
            raise ValueError(
                f"Value column '{column}' does not exist."
            )

    unpivoted = df.melt(
        id_vars=id_columns,
        value_vars=value_columns,
        var_name=task.get("variable_name", "Variable"),
        value_name=task.get("value_name", "Value")
    )

    unpivoted.to_excel(
        output_file,
        index=False
    )

    print("\nExcel unpivot complete.")
    print(f"ID columns    : {id_columns}")
    print(f"Value columns : {value_columns}")
    print(f"Rows before   : {len(df)}")
    print(f"Rows after    : {len(unpivoted)}")
    print(f"Output        : {output_file}")

    return {
        "success": True,
        "task_id": "012",
        "input": input_file,
        "output": output_file,
        "id_columns": id_columns,
        "value_columns": value_columns,
        "rows_before": len(df),
        "rows_after": len(unpivoted)
    }