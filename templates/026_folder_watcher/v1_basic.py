import time
from pathlib import Path


def run(task):

    watch_directory = Path(task["watch_directory"])
    interval = task.get("interval", 2)

    if not watch_directory.exists():
        watch_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    if not watch_directory.is_dir():
        raise ValueError(
            f"Watch path is not a directory: "
            f"{watch_directory}"
        )

    print("\nFolder watcher started.")
    print(f"Watching: {watch_directory}")
    print("Waiting for new .xlsx files...")
    print("Press Ctrl+C to stop.")

    known_files = {
        file.resolve()
        for file in watch_directory.glob("*.xlsx")
    }

    detected_files = []

    try:

        while True:

            current_files = {
                file.resolve()
                for file in watch_directory.glob("*.xlsx")
            }

            new_files = current_files - known_files

            for file in sorted(new_files):

                print(
                    f"\nNew Excel file detected: {file}"
                )

                detected_files.append(str(file))

            known_files = current_files

            time.sleep(interval)

    except KeyboardInterrupt:

        print("\nFolder watcher stopped.")

    return {
        "success": True,
        "task_id": "026",
        "watch_directory": str(watch_directory),
        "detected_files": detected_files,
        "files_detected": len(detected_files)
    }