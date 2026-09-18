import json
import importlib.util
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
REGISTRY_FILE = BASE_DIR / "registry" / "tasks.json"


def load_registry():
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_script(script_path):
    spec = importlib.util.spec_from_file_location(
        "automation_module",
        script_path
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def run_task(task_id, task):
    registry = load_registry()

    if task_id not in registry:
        raise ValueError(f"Unknown task ID: {task_id}")

    task_definition = registry[task_id]
    script_path = BASE_DIR / task_definition["script"]

    module = load_script(script_path)

    print(f"\nRunning: {task_definition['name']}")
    print(f"Task ID: {task_id}")

    return module.run(task)


if __name__ == "__main__":

    registry = load_registry()

    print("\n=== Excel Automation Vault ===\n")

    for task_id, task_info in registry.items():
        print(f"{task_id} - {task_info['name']}")
        print(f"     {task_info['description']}")

    print()

    task_id = input("Enter task ID: ").strip()

    if task_id not in registry:
        print(f"Unknown task ID: {task_id}")
        raise SystemExit(1)

    # ---------------------------------
    # Task-specific input collection
    # ---------------------------------

    if task_id in ["001", "002", "003", "006", "007", "009", "010"]:

        input_file = input("Enter input Excel file path: ").strip()
        output_file = input("Enter output Excel file path: ").strip()

        task = {
            "input": input_file,
            "output": output_file
        }

        # Task-specific parameters
        if task_id == "006":
            task["column"] = input(
                "Enter date column name: "
            ).strip()

        elif task_id == "009":
            task["column"] = input(
                "Enter column to filter: "
            ).strip()

            task["value"] = input(
                "Enter text to search for: "
            ).strip()

        elif task_id == "010":
            columns = input(
                "Enter text column names (comma separated): "
            ).strip()

            task["columns"] = [
                column.strip()
                for column in columns.split(",")
            ]

    elif task_id == "004":

        input_file_1 = input(
            "Enter FIRST Excel file path: "
        ).strip()

        input_file_2 = input(
            "Enter SECOND Excel file path: "
        ).strip()

        output_file = input(
            "Enter output Excel file path: "
        ).strip()

        task = {
            "input_1": input_file_1,
            "input_2": input_file_2,
            "output": output_file
        }

    elif task_id == "005":

        input_file = input(
            "Enter input Excel file path: "
        ).strip()

        column = input(
            "Enter column to split by: "
        ).strip()

        output_directory = input(
            "Enter output directory path: "
        ).strip()

        task = {
            "input": input_file,
            "column": column,
            "output_directory": output_directory
        }

    elif task_id == "008":

        input_file = input(
            "Enter input Excel file path: "
        ).strip()

        output_file = input(
            "Enter output Excel file path: "
        ).strip()

        old_name = input(
            "Enter column name to rename: "
        ).strip()

        new_name = input(
            "Enter new column name: "
        ).strip()

        task = {
            "input": input_file,
            "output": output_file,
            "rename_map": {
                old_name: new_name
            }
        }

    else:

        print(f"Task {task_id} is not yet configured in launcher.py.")
        raise SystemExit(1)

    # ---------------------------------
    # Execute task
    # ---------------------------------

    result = run_task(task_id, task)

    print("\n=== Result ===")
    print(result)