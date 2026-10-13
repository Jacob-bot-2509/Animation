"""Probe what answers on the target TCP port (diagnostic only)."""
import socket, sys, time
host, port = sys.argv[1], int(sys.argv[2])
for i in range(2):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    t = time.monotonic()
    try:
        code = s.connect_ex((host, port))
        el = (time.monotonic() - t) * 1000
        banner = b""
        if code == 0:
            s.settimeout(2)
            try:
                banner = s.recv(64)
            except socket.timeout:
                banner = b"<no-data-timeout>"
        print({"attempt": i, "errno": code, "elapsed_ms": round(el, 1),
               "first_bytes": banner[:64].decode("utf-8", "replace")})
    except OSError as exc:
        print({"attempt": i, "error": str(exc)})
    finally:
        s.close()
    time.sleep(0.3)
