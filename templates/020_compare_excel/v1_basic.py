import pandas as pd


def run(task):

    input_file_1 = task["input_1"]
    input_file_2 = task["input_2"]
    output_file = task["output"]
    key_column = task["key"]

    df_old = pd.read_excel(input_file_1)
    df_new = pd.read_excel(input_file_2)

    if key_column not in df_old.columns:
        raise ValueError(
            f"Key column '{key_column}' does not exist in first file."
        )

    if key_column not in df_new.columns:
        raise ValueError(
            f"Key column '{key_column}' does not exist in second file."
        )

    old_keys = set(df_old[key_column].dropna())
    new_keys = set(df_new[key_column].dropna())

    added_keys = new_keys - old_keys
    removed_keys = old_keys - new_keys
    common_keys = old_keys & new_keys

    added = df_new[
        df_new[key_column].isin(added_keys)
    ].copy()

    removed = df_old[
        df_old[key_column].isin(removed_keys)
    ].copy()

    # Detect changed records among common keys.
    common_old = (
        df_old[df_old[key_column].isin(common_keys)]
        .set_index(key_column)
        .sort_index()
    )

    common_new = (
        df_new[df_new[key_column].isin(common_keys)]
        .set_index(key_column)
        .sort_index()
    )

    changed_keys = []

    shared_columns = [
        column
        for column in common_old.columns
        if column in common_new.columns
    ]

    for key in common_keys:

        old_row = common_old.loc[key]
        new_row = common_new.loc[key]

        # Handle duplicate keys explicitly.
        if isinstance(old_row, pd.DataFrame):
            continue

        if isinstance(new_row, pd.DataFrame):
            continue

        different = False

        for column in shared_columns:

            old_value = old_row[column]
            new_value = new_row[column]

            if pd.isna(old_value) and pd.isna(new_value):
                continue

            if old_value != new_value:
                different = True
                break

        if different:
            changed_keys.append(key)

    changed_old = df_old[
        df_old[key_column].isin(changed_keys)
    ].copy()

    changed_new = df_new[
        df_new[key_column].isin(changed_keys)
    ].copy()

    # Write comparison report
    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        added.to_excel(
            writer,
            sheet_name="Added",
            index=False
        )

        removed.to_excel(
            writer,
            sheet_name="Removed",
            index=False
        )

        changed_old.to_excel(
            writer,
            sheet_name="Changed_Old",
            index=False
        )

        changed_new.to_excel(
            writer,
            sheet_name="Changed_New",
            index=False
        )

    print("\nExcel comparison complete.")
    print(f"Key column   : {key_column}")
    print(f"Added records : {len(added)}")
    print(f"Removed records: {len(removed)}")
    print(f"Changed records: {len(changed_keys)}")
    print(f"Output        : {output_file}")

    return {
        "success": True,
        "task_id": "020",
        "input_1": input_file_1,
        "input_2": input_file_2,
        "output": output_file,
        "key": key_column,
        "added": len(added),
        "removed": len(removed),
        "changed": len(changed_keys)
    }