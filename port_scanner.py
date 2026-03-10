import socket
import threading
from queue import Queue

THREADS = 100
queue = Queue()
print_lock = threading.Lock()


def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((target, port))

        if result == 0:
            with print_lock:
                print(f"[OPEN] Port {port}")

        s.close()

    except:
        pass


def worker(target):
    while True:
        port = queue.get()
        scan_port(target, port)
        queue.task_done()


def main():
    target_input = input("Enter target (IP or domain): ").strip()

    try:
        target = socket.gethostbyname(target_input)
    except socket.gaierror:
        print("❌ Invalid host")
        return

    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    print(f"\nScanning {target} from port {start_port} to {end_port}\n")

    for _ in range(THREADS):
        t = threading.Thread(target=worker, args=(target,))
        t.daemon = True
        t.start()

    for port in range(start_port, end_port + 1):
        queue.put(port)

    queue.join()

    print("\n✅ Scan completed.")


if __name__ == "__main__":
    main()
