"""最小 MCP stdio 客户端:通过 ai-bridge-mcp 的正式 tools/call 接口发送回信。

用法:
  python bridge_client.py list
  python bridge_client.py send <message.json>
message.json: {"from":..., "to":..., "type":..., "content":..., "metadata":{...}}
"""
import json
import subprocess
import sys
from pathlib import Path

NODE = r"C:\Program Files\nodejs\node.exe"
ENTRY = (r"C:\Users\Jacap\AppData\Local\npm-cache\_npx\364e919807c4833a"
         r"\node_modules\ai-bridge-mcp\dist\index.js")


def rpc(proc, payload):
    proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
    proc.stdin.flush()


def read_until(proc, want_id):
    while True:
        line = proc.stdout.readline()
        if not line:
            err = proc.stderr.read() if proc.poll() is not None else ""
            raise RuntimeError(f"bridge server closed before id={want_id}: {err[:500]}")
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if obj.get("id") == want_id:
            return obj


def open_session():
    proc = subprocess.Popen(
        [NODE, ENTRY],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", bufsize=1,
    )
    rpc(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "codex-dsh", "version": "1.0"},
    }})
    init = read_until(proc, 1)
    if "result" not in init:
        raise RuntimeError(f"initialize failed: {init}")
    rpc(proc, {"jsonrpc": "2.0", "method": "notifications/initialized"})
    rpc(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    tools = read_until(proc, 2)
    return proc, tools


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in ("list", "send"):
        print(__doc__)
        return 2
    proc, tools = open_session()
    try:
        if sys.argv[1] == "list":
            print(json.dumps(tools.get("result", {}), ensure_ascii=False, indent=2))
            return 0
        msg = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
        args = {k: msg[k] for k in ("from", "to", "type", "content")}
        if msg.get("metadata"):
            args["metadata"] = {str(k): str(v) for k, v in msg["metadata"].items()}
        rpc(proc, {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                   "params": {"name": "bridge_send", "arguments": args}})
        result = read_until(proc, 3)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if "result" in result and not result["result"].get("isError") else 1
    finally:
        try:
            proc.stdin.close()
            proc.terminate()
            proc.wait(timeout=10)
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
