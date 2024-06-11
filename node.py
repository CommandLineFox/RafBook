import socket
import threading


class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
        except ConnectionRefusedError:
            print(f"Error: Cannot connect to {self.host}:{self.port}")
            return
        self.lock = threading.Lock()
        self.files = {}
        self.friends = []
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        print(f"Node connected to {self.host}:{self.port}")

    def listen_for_messages(self):
        try:
            while True:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Received: {message.strip()}")
        except Exception as e:
            print(f"Listening error: {e}")

    def send_message(self, message):
        with self.lock:
            try:
                self.socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Sending message error: {e}")

    def add_friend(self, address, port):
        self.friends.append((address, port))
        print(f"Added friend: {address}:{port}")

    def add_file(self, path, visibility):
        self.files[path] = visibility
        print(f"Added file: {path} ({visibility})")

    def view_files(self, address, port):
        print(f"Files from {address}:{port}")
        for path, visibility in self.files.items():
            print(f"{path} ({visibility})")

    def remove_file(self, filename):
        if self.files.pop(filename, None):
            print(f"Removed file: {filename}")
        else:
            print(f"File not found: {filename}")

    def stop(self):
        self.socket.close()
        print("Node stopped")