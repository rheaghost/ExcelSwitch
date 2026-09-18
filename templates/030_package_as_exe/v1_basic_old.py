import pandas as pd
from pathlib import Path


def main():

    print("=== Excel Automation 030 ===")
    print("Simple Excel-to-Excel converter")
    print()

    input_file = input(
        "Enter input Excel file path: "
    ).strip()

    output_file = input(
        "Enter output Excel file path: "
    ).strip()

    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.is_file():
        print(
            f"\nERROR: Input file does not exist:\n"
            f"{input_path}"
        )
        input("\nPress Enter to exit...")
        return

    try:

        df = pd.read_excel(input_path)

        df.to_excel(
            output_path,
            index=False
        )

        print("\nProcessing complete.")
        print(f"Rows   : {len(df)}")
        print(f"Columns: {len(df.columns)}")
        print(f"Output : {output_path}")

    except Exception as exc:

        print("\nERROR:")
        print(str(exc))

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()