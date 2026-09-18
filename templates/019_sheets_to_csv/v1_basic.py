import pandas as pd
from pathlib import Path


def run(task):

    input_file = task["input"]
    output_directory = task["output_directory"]

    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    workbook = pd.read_excel(
        input_file,
        sheet_name=None
    )

    created_files = []

    for sheet_name, df in workbook.items():

        safe_name = str(sheet_name).strip()

        for char in '<>:"/\\|?*':
            safe_name = safe_name.replace(char, "_")

        output_file = output_dir / f"{safe_name}.csv"

        df.to_csv(
            output_file,
            index=False,
            encoding="utf-8-sig"
        )

        created_files.append(str(output_file))

    print("\nExcel sheets exported to CSV.")
    print(f"Sheets processed: {len(workbook)}")

    for file in created_files:
        print(f"  {file}")

    return {
        "success": True,
        "task_id": "019",
        "input": input_file,
        "output_directory": str(output_dir),
        "sheets_processed": len(workbook),
        "files_created": created_files
    }