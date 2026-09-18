import pandas as pd
from pathlib import Path


def run(task):

    input_file = task["input"]
    column = task["column"]
    output_directory = task["output_directory"]

    df = pd.read_excel(input_file)

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist."
        )

    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    created_files = []

    for value, group in df.groupby(
        column,
        dropna=False
    ):

        if pd.isna(value):
            safe_name = "blank"
        else:
            safe_name = str(value).strip()

        if not safe_name:
            safe_name = "blank"

        # Remove characters that are illegal in Windows filenames
        for char in '<>:"/\\|?*':
            safe_name = safe_name.replace(char, "_")

        output_file = output_dir / f"{safe_name}.xlsx"

        group.to_excel(
            output_file,
            index=False
        )

        created_files.append(str(output_file))

    print("\nExcel split complete.")
    print(f"Split column : {column}")
    print(f"Files created: {len(created_files)}")

    for file in created_files:
        print(f"  {file}")

    return {
        "success": True,
        "task_id": "005",
        "input": input_file,
        "column": column,
        "output_directory": str(output_dir),
        "files_created": created_files
    }