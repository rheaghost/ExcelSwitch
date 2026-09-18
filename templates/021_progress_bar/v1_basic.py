import pandas as pd
from tqdm import tqdm


def run(task):

    input_file = task["input"]
    output_file = task["output"]

    df = pd.read_excel(input_file)

    processed_rows = []

    print("\nProcessing rows...")

    for _, row in tqdm(
        df.iterrows(),
        total=len(df),
        desc="Processing"
    ):
        processed_rows.append(row)

    result_df = pd.DataFrame(processed_rows)

    result_df.to_excel(
        output_file,
        index=False
    )

    print("\nProcessing complete.")
    print(f"Rows processed: {len(result_df)}")
    print(f"Output        : {output_file}")

    return {
        "success": True,
        "task_id": "021",
        "input": input_file,
        "output": output_file,
        "rows_processed": len(result_df)
    }