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

    input_file = input("Enter Excel file path: ").strip()

    task = {
        "input": input_file
    }

    result = run_task("001", task)

    print("\nResult:")
    print(result)