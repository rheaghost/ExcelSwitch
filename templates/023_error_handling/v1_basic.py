import pandas as pd
from pathlib import Path


def run(task):

    input_file = task["input"]
    output_file = task["output"]
    required_column = task.get("required_column", "")

    try:
        # Check that the input file exists
        if not Path(input_file).is_file():
            raise FileNotFoundError(
                f"Input file does not exist: {input_file}"
            )

        # Try to read the workbook
        df = pd.read_excel(input_file)

        # Optional column validation
        if required_column:
            if required_column not in df.columns:
                raise ValueError(
                    f"Required column '{required_column}' "
                    f"does not exist."
                )

        # Try to write the output
        df.to_excel(
            output_file,
            index=False
        )

        print("\nError-handling task completed successfully.")
        print(f"Rows   : {len(df)}")
        print(f"Columns: {len(df.columns)}")
        print(f"Output : {output_file}")

        return {
            "success": True,
            "task_id": "023",
            "input": input_file,
            "output": output_file,
            "rows": len(df),
            "columns": len(df.columns),
            "error": None
        }

    except FileNotFoundError as exc:

        print("\nERROR: Input file not found.")
        print(str(exc))

        return {
            "success": False,
            "task_id": "023",
            "input": input_file,
            "output": output_file,
            "error_type": "FileNotFoundError",
            "error": str(exc)
        }

    except ValueError as exc:

        print("\nERROR: Invalid data or parameter.")
        print(str(exc))

        return {
            "success": False,
            "task_id": "023",
            "input": input_file,
            "output": output_file,
            "error_type": "ValueError",
            "error": str(exc)
        }

    except Exception as exc:

        print("\nERROR: Unexpected error.")
        print(str(exc))

        return {
            "success": False,
            "task_id": "023",
            "input": input_file,
            "output": output_file,
            "error_type": type(exc).__name__,
            "error": str(exc)
        }