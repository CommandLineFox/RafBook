import socket
import threading


class TcpServer:
    def __init__(self, host='localhost', port=3000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = []
        self.lock = threading.Lock()
        print(f"Server started on {self.host}:{self.port}")

    def start(self):
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                with self.lock:
                    self.clients.append(client_socket)
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Received: {message.strip()}")
                self.broadcast_message(message, client_socket)
        except Exception as e:
            print(f"Client handling error: {e}")
        finally:
            with self.lock:
                self.clients.remove(client_socket)
            client_socket.close()

    def broadcast_message(self, message, from_client):
        with self.lock:
            for client in self.clients:
                if client != from_client:
                    try:
                        client.send(message.encode('utf-8'))
                    except Exception as e:
                        print(f"Error sending message: {e}")


if __name__ == '__main__':
    server = TcpServer()
    server.start()