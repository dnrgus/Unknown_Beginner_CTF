import re
import socket
import sys


def recv_until(sock, marker):
    data = b""
    while marker not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data += chunk
    return data


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8201
    with socket.create_connection((host, port), timeout=5) as sock:
        recv_until(sock, b"password: ")
        sock.sendall(b"open_sesame_2026\n")
        data = sock.recv(4096).decode(errors="replace")
    flag = re.search(r"UNKNOWN\{[^}]+\}", data)
    if not flag:
        raise SystemExit("flag not found")
    print(flag.group(0))


if __name__ == "__main__":
    main()
