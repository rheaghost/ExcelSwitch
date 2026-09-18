import shutil
from datetime import datetime
from pathlib import Path


def run(task):

    source_directory = Path(task["source_directory"])
    backup_directory = Path(task["backup_directory"])

    if not source_directory.exists():
        raise FileNotFoundError(
            f"Source directory does not exist: {source_directory}"
        )

    if not source_directory.is_dir():
        raise ValueError(
            f"Source path is not a directory: {source_directory}"
        )

    # Create a YYYY-MM-DD backup folder.
    date_folder = datetime.now().strftime("%Y-%m-%d")
    destination_directory = (
        backup_directory / date_folder
    )

    destination_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    source_files = list(
        source_directory.glob("*.xlsx")
    )

    copied_files = []

    for source_file in source_files:

        destination_file = (
            destination_directory / source_file.name
        )

        shutil.copy2(
            source_file,
            destination_file
        )

        copied_files.append(
            str(destination_file)
        )

    print("\nBackup complete.")
    print(f"Source directory : {source_directory}")
    print(f"Backup directory : {destination_directory}")
    print(f"Files copied     : {len(copied_files)}")

    for file in copied_files:
        print(f"  {file}")

    return {
        "success": True,
        "task_id": "027",
        "source_directory": str(source_directory),
        "backup_directory": str(destination_directory),
        "files_copied": copied_files,
        "files_count": len(copied_files)
    }