import threading
import time
import yaml
from tcp.server import TcpServer
from tcp.node import Node


def start_server(server_config):
    server = TcpServer(port=server_config['port'])
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    return server_thread


def start_node(config, port):
    node = Node(config, port)
    node_thread = threading.Thread(target=lambda: None, daemon=True)  # Dummy thread to keep node active
    node_thread.start()
    return node, node_thread


def main():
    with open('config.yml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    start_server(config['bootstrap'])
    time.sleep(1)

    nodes = []
    node_threads = []
    for servent in config['servents']:
        port = servent['port']
        node, node_thread = start_node(config, port)
        nodes.append(node)
        node_threads.append(node_thread)
        time.sleep(0.5)

    print("Server and nodes are running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping server and nodes...")


if __name__ == '__main__':
    main()
