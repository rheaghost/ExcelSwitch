import pandas as pd


def run(task):

    input_file = task["input"]
    output_file = task["output"]

    replacements = task.get(
        "values",
        ["N/A", "n/a", "NA"]
    )

    # Prevent pandas from automatically converting
    # N/A / NA / n/a to NaN while reading.
    df = pd.read_excel(
        input_file,
        keep_default_na=False
    )

    replacement_count = 0

    for value in replacements:
        replacement_count += int(
            (df == value).sum().sum()
        )

    df = df.replace(replacements, pd.NA)

    df.to_excel(
        output_file,
        index=False
    )

    print("\nN/A replacement complete.")
    print(f"Values replaced : {replacements}")
    print(f"Replacements    : {replacement_count}")
    print(f"Output          : {output_file}")

    return {
        "success": True,
        "task_id": "014",
        "input": input_file,
        "output": output_file,
        "values_replaced": replacements,
        "replacement_count": replacement_count
    }