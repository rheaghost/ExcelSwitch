import shutil
from pathlib import Path


def main():

    print("=== Excel Automation 030 ===")
    print("Standalone Excel workbook copier")
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

    if input_path.suffix.lower() != ".xlsx":
        print(
            "\nERROR: This V1 program accepts .xlsx files only."
        )
        input("\nPress Enter to exit...")
        return

    if output_path.suffix.lower() != ".xlsx":
        print(
            "\nERROR: Output file must have a .xlsx extension."
        )
        input("\nPress Enter to exit...")
        return

    if input_path.resolve() == output_path.resolve():
        print(
            "\nERROR: Input and output files must be different."
        )
        input("\nPress Enter to exit...")
        return

    try:

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(
            input_path,
            output_path
        )

        print("\nWorkbook copied successfully.")
        print(f"Input : {input_path}")
        print(f"Output: {output_path}")
        print()
        print(
            "The workbook structure is preserved, "
            "including its worksheets and embedded chart objects."
        )

    except Exception as exc:

        print("\nERROR:")
        print(str(exc))

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()