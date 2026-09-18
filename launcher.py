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


def collect_parameters(task_definition):

    task = {}

    print("\nEnter task parameters:\n")

    for parameter in task_definition["parameters"]:

        name = parameter["name"]
        label = parameter["label"]
        parameter_type = parameter["type"]

        if parameter_type == "rename_map":

            old_name = input(
                "Enter existing column name: "
            ).strip()

            new_name = input(
                "Enter new column name: "
            ).strip()

            value = {
                old_name: new_name
            }

        else:

            value = input(
                f"{label}: "
            ).strip()

            if parameter_type == "integer":
                value = int(value)

            elif parameter_type == "float":
                value = float(value)
                
                
            elif parameter_type == "text_list":
                value = [
                    item.strip()
                    for item in value.split(",")
                    if item.strip()
                ]

            elif parameter_type == "rename_map":
                old_name = input(
                    "Enter existing column name: "
                ).strip()

                new_name = input(
                    "Enter new column name: "
                ).strip()

                value = {
                    old_name: new_name
                }   

        task[name] = value

    return task

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

        print(
            f"{task_id} - "
            f"{task_info['name']}"
        )

        print(
            f"     {task_info['description']}"
        )

    print()

    task_id = input("Enter task ID: ").strip()

    if task_id not in registry:

        print(f"Unknown task ID: {task_id}")
        raise SystemExit(1)

    task_definition = registry[task_id]

    task = collect_parameters(task_definition)

    result = run_task(task_id, task)

    print("\n=== Result ===")
    print(result)