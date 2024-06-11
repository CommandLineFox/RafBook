import socket
import threading


class Node:
    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            threading.Thread(target=self.listen_for_messages, daemon=True).start()
        except ConnectionRefusedError:
            print(f"Error: Cannot connect to server at {self.host}:{self.port}")

    def listen_for_messages(self):
        try:
            while True:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Received: {message.strip()}")
        except Exception as e:
            print(f"Listening error: {e}")

    def send_message(self, message):
        try:
            self.socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Sending message error: {e}")

    def stop(self):
        self.socket.close()
        print("Node stopped")


if __name__ == '__main__':
    pass
