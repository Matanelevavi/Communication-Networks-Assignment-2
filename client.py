# client.py
import argparse, socket, json, sys

def request(s: socket.socket, payload: dict) -> dict:
    """Send a single JSON-line request and return a single JSON-line response."""
    data = (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")

    s.sendall(data)
    buff = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        buff += chunk
        if b"\n" in buff:
            line, _, _ = buff.partition(b"\n")
            return json.loads(line.decode("utf-8"))
    return {"ok": False, "error": "No response"}

def main():
    ap = argparse.ArgumentParser(description="Client (calc/gpt over JSON TCP)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5554)
    ap.add_argument("--mode", choices=["calc", "gpt"])
    ap.add_argument("--expr", help="Expression for mode=calc")
    ap.add_argument("--prompt", help="Prompt for mode=gpt")
    ap.add_argument("--no-cache", action="store_true", help="Disable caching")
    args = ap.parse_args()

    try:
        with socket.create_connection((args.host, args.port)) as s:

            if args.mode:
                print(f"Connected to {args.host}:{args.port} (One-Shot Mode)")

                if args.mode == "calc":
                    if not args.expr:
                        print("Missing --expr", file=sys.stderr);
                        sys.exit(2)
                    payload = {"mode": "calc", "data": {"expr": args.expr}, "options": {"cache": not args.no_cache}}
                else:
                    if not args.prompt:
                        print("Missing --prompt", file=sys.stderr);
                        sys.exit(2)
                    payload = {"mode": "gpt", "data": {"prompt": args.prompt}, "options": {"cache": not args.no_cache}}

                resp = request(s, payload)
                print(json.dumps(resp, ensure_ascii=False, indent=2))
                return

            print(f"Connected to {args.host}:{args.port} (Interactive Mode)")
            print("Type 'quit' to exit.")
            while True:
                mode = input("\nMode (calc/gpt): ").strip()
                if mode in ["quit", "exit"]:
                    print("Disconnecting from server!")
                    break

                if mode == "calc":
                    expr = input("Expression: ").strip()
                    if not expr: continue
                    payload = {"mode": "calc", "data": {"expr": expr}, "options": {"cache": not args.no_cache}}
                elif mode == "gpt":
                    prompt = input("Prompt: ").strip()
                    if not prompt: continue
                    payload = {"mode": "gpt", "data": {"prompt": prompt}, "options": {"cache": not args.no_cache}}
                else:
                    print("Unknown mode")
                    continue

                try:
                    resp = request(s, payload)
                    print(json.dumps(resp, ensure_ascii=False, indent=2))
                except Exception as e:
                    print(f"Error: {e}")
                    break
    except ConnectionRefusedError:
        print("Error: Could not connect to server.")

if __name__ == "__main__":
    main()
