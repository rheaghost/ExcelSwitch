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

    input_file = input("Enter Excel file path: ").strip()

    task = {
        "input": input_file
    }

    # 002 and future tasks may need an output filename.
    if task_id != "001":
        output_file = input("Enter output file path: ").strip()
        task["output"] = output_file

    result = run_task(task_id, task)

    print("\n=== Result ===")
    print(result)