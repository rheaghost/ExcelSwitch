# excel_tools.py - MCP-ready wrappers around launcher.run_task (260927HHMM)
#
# Two functions exposed to the AI:
#   list_tasks(category)     - discover what tasks are available
#   execute(task_id, params) - run a task
#
# The templates and launcher are unchanged. This file just wraps them
# with a stable contract for the MCP layer above.

import io
from contextlib import redirect_stdout
from launcher import run_task, load_registry


def list_tasks(category: str = "all") -> list:
    """Return available tasks with IDs, names, descriptions, params.

    Args:
        category: "clean", "transform", "read", "analyze", "deliver",
                  "convert", "ops", or "all"

    Returns:
        List of dicts. Dev-only tools (category "dev") are excluded.
    """
    registry = load_registry()
    out = []
    for tid, meta in registry.items():
        cat = meta.get("category", "")
        if cat == "dev":
            continue
        if category != "all" and cat != category:
            continue
        out.append({
            "id": tid,
            "name": meta["name"],
            "description": meta["description"],
            "category": cat,
            "params": [p["name"] for p in meta["parameters"]],
        })
    return out


def execute(task_id: str, params: dict) -> dict:
    """Run a task by ID and return its result dict.

    All stdout produced by the template and launcher is captured and
    attached as '_log' in the result, so callers can choose to display
    or ignore it. This also keeps stdout clean for the MCP protocol.
    """
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            result = run_task(task_id, params)
        if isinstance(result, dict):
            result["_log"] = buf.getvalue()
            return result
        return {"success": True, "result": result, "_log": buf.getvalue()}
    except Exception as e:
        return {"success": False, "error": str(e), "_log": buf.getvalue()}