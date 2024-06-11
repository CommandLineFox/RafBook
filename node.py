import os
import socket
import threading

import yaml


def hash_key(key, chord_size):
    return key * 97 % chord_size

class Node:
    def __init__(self, config_path, port):
        self.load_config(config_path)
        self.port = port
        self.id = hash_key(self.port, self.chord_size)
        self.finger_table = [None] * 6
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.bootstrap_ip, self.bootstrap_port))
        except ConnectionRefusedError:
            print(f"Error: Cannot connect to {self.bootstrap_ip}:{self.bootstrap_port}")
            return
        self.lock = threading.Lock()
        self.files = {}
        self.friends = []
        self.ensure_working_root_exists()
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        self.initialize_finger_table()
        print(f"Node connected to {self.bootstrap_ip}:{self.bootstrap_port} with ID {self.id}")

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            self.working_root = os.path.abspath(config['working_root'])
            self.bootstrap_ip = config['bootstrap']['ip']
            self.bootstrap_port = config['bootstrap']['port']
            self.chord_size = config['chord_size']

    def ensure_working_root_exists(self):
        if not os.path.exists(self.working_root):
            os.makedirs(self.working_root)

    def initialize_finger_table(self):
        for i in range(6):
            start = (self.id + 2 ** i) % self.chord_size
            self.finger_table[i] = self.find_successor(start)

    def find_successor(self, id):
        if id >= self.id:
            return (self.host, self.port)
        else:
            return (self.bootstrap_ip, self.bootstrap_port)

    def listen_for_messages(self):
        try:
            while True:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Received: {message.strip()}")
                    self.handle_message(message.strip())
        except Exception as e:
            print(f"Listening error: {e}")

    def handle_message(self, message):
        print(f"Handling message: {message}")

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
        if os.path.exists(path):
            with open(path, 'r') as file:
                content = file.read()
            file_name = os.path.basename(path)
            self.files[file_name] = {'content': content, 'visibility': visibility}
            print(f"Added file: {file_name} ({visibility})")
        else:
            print(f"File not found: {path}")

    def view_files(self, address, port):
        print(f"Files from {address}:{port}")
        for path, file_info in self.files.items():
            print(f"{path} ({file_info['visibility']})")

    def remove_file(self, filename):
        if self.files.pop(filename, None):
            print(f"Removed file: {filename}")
        else:
            print(f"File not found: {filename}")

    def stop(self):
        self.socket.close()
        print("Node stopped")
