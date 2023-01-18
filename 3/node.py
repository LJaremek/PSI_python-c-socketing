from threading import Thread
import pickle
from socket import AF_INET, SOCK_STREAM, SO_BROADCAST, SOL_SOCKET, SO_REUSEADDR, SOCK_DGRAM
from socket import socket
import json
import os
import shutil

from datatypes import DownloadRequest, BroadcastMessage

IS_UDP_THREAD_RUNNING = True


def udp_server_thread(udp_socket, node):
    global IS_UDP_THREAD_RUNNING
    while IS_UDP_THREAD_RUNNING:
        file_names = []
        data = pickle.loads(udp_socket.recv(1024))
        if any(x.node_addr == data.node_addr for x in node.available_files):
            for x in node.available_files:
                if x.node_addr == data.node_addr:
                    x.resources = data.resources
        else:
            node.available_files.append(BroadcastMessage(data.node_addr, data.resources))
        for file in node.available_files:
            file_names.extend(file.resources)
        node._available_file_names = list(dict.fromkeys(file_names))


def tcp_server_thread_function(tcp_socket, node):
    while True:
        tcp_socket.listen()
        conn, addr = tcp_socket.accept()
        data = conn.recv(1024)
        request = pickle.loads(data)
        filename = request.filename
        if filename not in node.downloaded_files():
            conn.send(bytes("no such file in this node", 'utf-8'))
            continue
        with open(f"node_data/{filename}", "rb") as f:
            for chunk in iter(lambda: f.read(1024), b''):
                conn.sendall(chunk)
        conn.close()


def tcp_client_thread_function(client_socket, file_name, node):
    with open(f"./node_data/{file_name}", 'wb') as f:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)
    node._file_during_download = ""
    client_socket.close()
    data = BroadcastMessage(node.node_addr, node.downloaded_files())
    node.update_file_list(data)


class Socket(socket):
    def __init__(self, node_name: str, *args, **kwargs) -> None:
        super(Socket, self).__init__(*args, **kwargs)
        self._name = node_name

    @property
    def name(self) -> str:
        return self._name


class Node:
    def __init__(
            self,
            node_name: str,
            node_addr: str,
            node_port: int,
            config_file_path: str = "config.json"
    ) -> None:

        self.node_addr = node_addr
        self._config_data = self._read_config_file(config_file_path)
        self._nodes: list[dict] = self._config_data["nodes"]
        self._tcp_socket: Socket

        self.udp_thread = None
        self._create_server_socket(node_name, node_addr, node_port)

        self._client_sockets: list[Socket] = []
        self._client_socket: Socket
        self.available_files: list[BroadcastMessage] = []

        self._available_file_names: list[str] = []
        for file in self.available_files:
            self._available_file_names.extend(file.resources)
        self._available_file_names = list(dict.fromkeys(self._available_file_names))
        self._file_during_download: str = ""
        self._packet_loss = False

    def imitate_packet_loss(self) -> None:
        self._packet_loss = True

    def kill_udp_thread(self):
        global IS_UDP_THREAD_RUNNING
        IS_UDP_THREAD_RUNNING = False

    def _read_config_file(self, config_file_path: str) -> list[dict]:
        with open(config_file_path, "r", -1, "utf-8") as f:
            return json.load(f)

    def _create_server_socket(
            self,
            node_name: str,
            node_addr: str,
            node_port: int,
    ) -> socket:

        self._server_socket = Socket(node_name, AF_INET, SOCK_DGRAM)
        self._server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._server_socket.bind((node_addr, node_port))
        self.udp_thread = Thread(target=udp_server_thread, args=(self._server_socket, self))
        self.udp_thread.start()

        self._tcp_socket = Socket(node_name, AF_INET, SOCK_STREAM)
        self._tcp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._tcp_socket.bind((node_addr, node_port))
        tcp_server_thread = Thread(target=tcp_server_thread_function, args=(self._tcp_socket, self))
        tcp_server_thread.start()

    def get_available_files(self) -> list[str]:
        return self._available_file_names

    def downloaded_files(self) -> list[str]:
        return [
            file_name for file_name in os.listdir("./node_data/")
            if file_name != ".gitkeep"
        ]

    def update_file_list(self, data) -> None:
        if not self._packet_loss:
            for node in self._nodes:
                pb = pickle.dumps(data)
                self._server_socket.sendto(pb, (node["node_addr"], node["node_port"]))
        else:
            self._packet_loss = False

    def upload_file(self, file_path: str) -> None:
        if file_path[0] == "~":
            file_path = os.path.expanduser(file_path)
        if not os.path.isfile(file_path):
            print("File does not exist")
            return
        file_name = os.path.basename(file_path)
        if file_name in self.downloaded_files():
            print("File already exists")
            return
        shutil.copy(file_path, f"./node_data/{file_name}")
        data = BroadcastMessage(self.node_addr, self.downloaded_files())
        self.update_file_list(data)
        ...

    def _list_file_owners(self, file_name: str) -> list[str]:
        owners_addrs = []
        owners = []
        for file in self.available_files:
            if file_name in file.resources:
                owners_addrs.append(file.node_addr)
        for node in self._nodes:
            if node["node_addr"] in owners_addrs:
                owners.append(node["node_name"])
        return owners

    def download_file(self, file_name: str) -> None:
        if file_name in self.downloaded_files():
            print("File already exists")
            return
        if file_name not in self._available_file_names:
            print("File does not exist")
            return None
        print(self._list_file_owners(file_name))
        node_name = input("Choose node to download from: ")
        if node_name not in self._list_file_owners(file_name):
            print("Wrong node name")
            return None
        for node in self._nodes:
            if node["node_name"] == node_name:
                node_addr = node["node_addr"]
                node_port = node["node_port"]
        request = DownloadRequest(file_name)

        client_socket = Socket(node_name, AF_INET, SOCK_STREAM)
        client_socket.connect((node_addr, node_port))
        client_socket.sendall(pickle.dumps(request))
        self._file_during_download = file_name
        tcp_server_thread = Thread(target=tcp_client_thread_function, args=(client_socket, file_name, self))
        tcp_server_thread.start()

    def download_progress(self, file_name) -> str:
        if file_name != self._file_during_download and file_name not in self.downloaded_files():
            return "File is not being downloaded"
        if file_name in self.downloaded_files():
            return "File is already downloaded"
        return "File is being downloaded"
