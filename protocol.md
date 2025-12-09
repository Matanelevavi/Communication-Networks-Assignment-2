# Protocol Documentation

My project uses a simple protocol based on JSON over TCP.
Every message is a single line of text that ends with a newline character (`\n`).

## 1. Request Format (Client sends to Server)
The client sends a JSON object with 3 fields:
* **mode**: What operation to run (`"calc"` or `"gpt"`).
* **data**: The input for the command (like `"expr"` or `"prompt"`).
* **options**: Settings like `"cache": true`.

**Example:**
`{"mode": "calc", "data": {"expr": "1+1"}, "options": {"cache": true}}`

## 2. Response Format (Server sends to Client)
The server replies with a JSON object containing:
* **ok**: `true` if successful, `false` if there was an error.
* **result**: The answer from the server.
* **meta**: Extra info, like `from_cache` or `took_ms`.

**Example:**
`{"ok": true, "result": 2.0, "meta": {"from_cache": false}}`