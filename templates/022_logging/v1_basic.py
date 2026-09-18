import pandas as pd
from datetime import datetime
from pathlib import Path


def write_log(log_file, message):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(
        log_file,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"{timestamp} - {message}\n"
        )


def run(task):

    input_file = task["input"]
    output_file = task["output"]
    log_file = task["log_file"]

    # Make sure the log directory exists
    Path(log_file).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    write_log(
        log_file,
        "START"
    )

    write_log(
        log_file,
        f"Input: {input_file}"
    )

    try:

        df = pd.read_excel(input_file)

        write_log(
            log_file,
            f"Rows: {len(df)}"
        )

        write_log(
            log_file,
            f"Columns: {len(df.columns)}"
        )

        write_log(
            log_file,
            f"Column names: {list(df.columns)}"
        )

        df.to_excel(
            output_file,
            index=False
        )

        write_log(
            log_file,
            f"Output: {output_file}"
        )

        write_log(
            log_file,
            "COMPLETE"
        )

        print("\nLogging task complete.")
        print(f"Rows      : {len(df)}")
        print(f"Columns   : {len(df.columns)}")
        print(f"Output    : {output_file}")
        print(f"Log file  : {log_file}")

        return {
            "success": True,
            "task_id": "022",
            "input": input_file,
            "output": output_file,
            "log_file": log_file,
            "rows": len(df),
            "columns": len(df.columns)
        }

    except Exception as exc:

        write_log(
            log_file,
            f"ERROR: {exc}"
        )

        write_log(
            log_file,
            "FAILED"
        )

        raise