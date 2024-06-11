import threading
from tcp.server import TcpServer


def main():
    server = TcpServer()
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()

    print("Server is running. Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping server...")


if __name__ == '__main__':
    main()
