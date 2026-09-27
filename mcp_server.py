# mcp_server.py - Minimal MCP server over HTTP (260927HHMM)
#
# Implements the MCP subset the AI Secretary app needs:
#   initialize    - handshake
#   tools/list    - return available tools
#   tools/call    - execute a tool by name
#
# Transport: HTTP POST to /mcp with JSON-RPC 2.0 body.
# Run: python mcp_server.py
# Test: curl -X POST http://localhost:8765/mcp -d '{...}'

import json
from flask import Flask, request, jsonify
from excel_tools import list_tasks, execute,list_sample_files


app = Flask(__name__)

# Tool registry — name -> (description, input schema, handler)
def _schema(**props):
    return {
        "type": "object",
        "properties": {
            k: {"type": v} if isinstance(v, str) else v
            for k, v in props.items()
        }
    }

TOOLS = {
    "list_tasks": {
        "description": "List available Excel tasks. Optionally filter by category.",
        "inputSchema": _schema(category="string"),
        "handler": lambda args: list_tasks(args.get("category", "all")),
    },
    "execute": {
        "description": "Run an Excel task by ID with parameters.",
        "inputSchema": _schema(task_id="string", params="object"),
        "handler": lambda args: execute(args["task_id"], args.get("params", {})),
    },
        "list_sample_files": {
        "description": "List all sample Excel files available on the server.",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": lambda args: list_sample_files(),
    },
}


@app.route("/mcp", methods=["POST"])
def mcp():
    body = request.get_json(force=True)
    req_id = body.get("id")
    method = body.get("method")
    params = body.get("params", {})

    try:
        if method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "excel-switch", "version": "1.0"},
                "capabilities": {"tools": {}},
            }
        elif method == "tools/list":
            result = {"tools": [
                {"name": name, "description": t["description"], "inputSchema": t["inputSchema"]}
                for name, t in TOOLS.items()
            ]}
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            if tool_name not in TOOLS:
                return jsonify({
                    "jsonrpc": "2.0", "id": req_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
                })
            output = TOOLS[tool_name]["handler"](tool_args)
            result = {
                "content": [{"type": "text", "text": json.dumps(output, ensure_ascii=False, indent=2)}]
            }
        else:
            return jsonify({
                "jsonrpc": "2.0", "id": req_id,
                "error": {"code": -32601, "message": f"Unknown method: {method}"},
            })

        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})

    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0", "id": req_id,
            "error": {"code": -32603, "message": str(e)},
        })


if __name__ == "__main__":
    print("MCP server starting on http://0.0.0.0:8765/mcp")
    app.run(host="0.0.0.0", port=8765, debug=False)