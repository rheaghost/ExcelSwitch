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
from pathlib import Path

def _resolve_old(path: str) -> str:
    """Make a path absolute. Relative paths resolve against ROOT.
    Also handles the common case where the model sends just a folder name."""
    if not path:
        return path
    p = Path(path)
    if p.is_absolute():
        return str(p)
    # Try: ROOT / path
    candidate = ROOT / path
    if candidate.exists():
        return str(candidate)
    # Try: ROOT / templates / path  (model often omits "templates")
    candidate = ROOT / "templates" / path
    if candidate.exists():
        return str(candidate)
    # Fall back: ROOT / path anyway (let the template error out if wrong)
    return str(candidate)

#
def _resolve(path: str) -> str:
    """Resolve a path to an actual file on disk (260927HHMM).

    Order of attempts:
      1. If absolute and exists, use as-is.
      2. Try ROOT / path.
      3. Try ROOT / "templates" / path.
      4. Recursively search ROOT for the filename.
      5. Fall back to ROOT / path (template will error with a clear message).
    """
    if not path:
        return path
    p = Path(path)

    # 1. Absolute
    if p.is_absolute():
        if p.exists():
            return str(p)
        # Absolute but missing — still try recursive search by name below
        filename = p.name
    else:
        # 2. ROOT / path
        c = ROOT / path
        if c.exists():
            return str(c)
        # 3. ROOT / templates / path
        c = ROOT / "templates" / path
        if c.exists():
            return str(c)
        filename = p.name

    # 4. Recursive search by filename
    if filename:
        for found in ROOT.rglob(filename):
            return str(found)

    # 5. Give up — return best guess so template can error meaningfully
    if p.is_absolute():
        return str(p)
    return str(ROOT / "templates" / path)
#

# Server root — where this file lives (260927HHMM)
ROOT = Path(__file__).resolve().parent


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


def execute_old(task_id: str, params: dict) -> dict:
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
    
def execute(task_id: str, params: dict) -> dict:
    """Run a task by ID or name and return its result dict.

    Accepts either the numeric ID ("002") or the name ("remove_duplicates").
    All stdout produced by the template and launcher is captured and
    attached as '_log' in the result.
    """
    # Resolve name -> ID if needed (260927HHMM)
    registry = load_registry()
    resolved_id = task_id
    if task_id not in registry:
        # Search by name (case-insensitive, partial match allowed)
        needle = task_id.lower().strip()
        for tid, meta in registry.items():
            if meta.get("name", "").lower() == needle:
                resolved_id = tid
                break
        else:
            # Partial match fallback
            for tid, meta in registry.items():
                if needle in meta.get("name", "").lower():
                    resolved_id = tid
                    break

    buf = io.StringIO()
    
    #
    # Resolve relative paths against the server root (260927HHMM)
    resolved_params = dict(params)
    # resolve part
        # Resolve input paths (search disk), then place outputs next to input (260927HHMM)
    resolved_params = dict(params)

    # 1. Resolve inputs first
    for key in ("input", "input_1", "input_2"):
        if key in resolved_params and isinstance(resolved_params[key], str):
            resolved_params[key] = _resolve(resolved_params[key])

    # 2. For outputs, use input's parent directory when only a bare filename was given
    input_dir = None
    for key in ("input", "input_1"):
        if key in resolved_params:
            input_dir = str(Path(resolved_params[key]).parent)
            break

    for key in ("output", "log_file"):
        if key not in resolved_params or not isinstance(resolved_params[key], str):
            continue
        p = Path(resolved_params[key])
        if p.is_absolute():
            continue  # user gave full path — respect it
        if input_dir:
            resolved_params[key] = str(Path(input_dir) / p.name)
        else:
            resolved_params[key] = _resolve(resolved_params[key])

    # 3. Directory params keep the old search behavior
    for key in ("output_directory", "directory"):
        if key in resolved_params and isinstance(resolved_params[key], str):
            resolved_params[key] = _resolve(resolved_params[key])
    
    
    # end resolve part
    try:
        with redirect_stdout(buf):
           
            result = run_task(resolved_id, resolved_params)
        if isinstance(result, dict):
            result["_log"] = buf.getvalue()
            return result
        return {"success": True, "result": result, "_log": buf.getvalue()}
    except Exception as e:
        return {"success": False, "error": str(e), "_log": buf.getvalue()}
    
def list_sample_files() -> list:
    """List sample Excel files available in the templates folder (260927HHMM)."""
    out = []
    templates = ROOT / "templates"
    if not templates.exists():
        return out
    for xlsx in templates.rglob("*.xlsx"):
        rel = xlsx.relative_to(ROOT)
        out.append(str(rel).replace("\\", "/"))
    return sorted(out)
