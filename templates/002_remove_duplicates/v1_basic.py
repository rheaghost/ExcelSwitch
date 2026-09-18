import pandas as pd


def run(task):

    input_file = task["input"]
    output_file = task.get("output", "cleaned.xlsx")

    df = pd.read_excel(input_file)

    before = len(df)

    df_clean = df.drop_duplicates()

    after = len(df_clean)
    removed = before - after

    df_clean.to_excel(output_file, index=False)

    print("\nDuplicate removal complete.")
    print(f"Original rows : {before}")
    print(f"Final rows    : {after}")
    print(f"Removed       : {removed}")
    print(f"Output file   : {output_file}")

    return {
        "success": True,
        "task_id": "002",
        "input": input_file,
        "output": output_file,
        "original_rows": before,
        "final_rows": after,
        "removed_rows": removed
    }