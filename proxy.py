# proxy.py
import argparse, socket, threading, json,collections

class LRUCache:
    """Minimal LRU cache based on OrderedDict."""
    def __init__(self, capacity: int = 128):
        self.capacity = capacity
        self._d = collections.OrderedDict()

    def get(self, key):
        if key not in self._d:
            return None
        self._d.move_to_end(key)
        return self._d[key]

    def set(self, key, value):
        self._d[key] = value
        self._d.move_to_end(key)
        if len(self._d) > self.capacity:
            self._d.popitem(last=False)


def main():
    ap = argparse.ArgumentParser(description="Transparent TCP proxy (optional)")
    ap.add_argument("--listen-host", default="127.0.0.1")
    ap.add_argument("--listen-port", type=int, default=5554)
    ap.add_argument("--server-host", default="127.0.0.1")
    ap.add_argument("--server-port", type=int, default=5555)
    args = ap.parse_args()

    cache = LRUCache(128)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((args.listen_host, args.listen_port))
        s.listen(16)
        print(f"[proxy] {args.listen_host}:{args.listen_port} -> {args.server_host}:{args.server_port}")
        while True:
            c, addr = s.accept()
            threading.Thread(target=handle, args=(c, args.server_host, args.server_port, cache), daemon=True).start()

def handle(c, sh, sp, cache):
    with c:
        try:
            with socket.create_connection((sh, sp)) as s:
                buffer = b""
                while True:
                    data = c.recv(1024)
                    if not data: break
                    buffer += data

                    while b"\n" in buffer:
                        line, _, rest = buffer.partition(b"\n")
                        buffer = rest
                        if not line.strip(): continue

                        request_str = line.decode("utf-8")
                        cached_response = cache.get(request_str)

                        if cached_response:
                            print(f"[proxy] Cache HIT {request_str.strip()}")
                            cached_response["meta"]["from_proxy"] = True
                            c.sendall((json.dumps(cached_response) + "\n").encode("utf-8"))
                        else:
                            print(f"[proxy] Cache MISS: {request_str.strip()}")
                            s.sendall(line+b"\n")

                            server_response = s.recv(4096)
                            if not server_response:
                                break
                            c.sendall(server_response)

                            try:
                                resp_json = json.loads(server_response.decode("utf-8"))
                                cache.set(request_str, resp_json)
                            except:
                                pass

        except Exception as e:
            try: c.sendall((json.dumps({"ok": False, "error": f"Proxy error: {e}"})+"\n").encode("utf-8"))
            except Exception: pass

if __name__ == "__main__":
    main()
