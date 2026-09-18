import pandas as pd


def run(task):

    input_file = task["input"]
    output_file = task["output"]

    index_column = task["index_column"]
    columns_column = task["columns_column"]
    values_column = task["values_column"]
    aggfunc = task.get("aggfunc", "sum")

    df = pd.read_excel(input_file)

    required_columns = [
        index_column,
        columns_column,
        values_column
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Column '{column}' does not exist."
            )

    pivot = pd.pivot_table(
        df,
        index=index_column,
        columns=columns_column,
        values=values_column,
        aggfunc=aggfunc,
        fill_value=0
    )

    pivot = pivot.reset_index()

    pivot.to_excel(
        output_file,
        index=False
    )

    print("\nPivot table created.")
    print(f"Index column   : {index_column}")
    print(f"Columns column : {columns_column}")
    print(f"Values column  : {values_column}")
    print(f"Aggregation    : {aggfunc}")
    print(f"Output         : {output_file}")

    return {
        "success": True,
        "task_id": "013",
        "input": input_file,
        "output": output_file,
        "index_column": index_column,
        "columns_column": columns_column,
        "values_column": values_column,
        "aggfunc": aggfunc
    }