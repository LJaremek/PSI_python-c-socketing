from threading import Thread
import pickle
from socket import AF_INET, SOCK_STREAM, SO_BROADCAST, SOL_SOCKET, SO_REUSEADDR, SOCK_DGRAM
from socket import socket
import json
import os
import shutil

from datatypes import DownloadRequest, BroadcastMessage


def udp_server_thread(udp_socket):
    while True:
        data = pickle.loads(udp_socket.recv(1024))
        print(f"Python server received : {data.node_addr} {data.resources}")
        # TODO handle data


def tcp_server_thread_function(tcp_socket, node):
    while True:
        tcp_socket.listen()
        conn, addr = tcp_socket.accept()
        data = conn.recv(1024)
        request = DownloadRequest(data)
        filename = request.filename.decode("utf-8").strip()
        print(node.downloaded_files())
        print(f"filename: {filename}")
        if filename not in node.downloaded_files():
            conn.send("no such file in this node")
        # TODO wysyłka pliku


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
            node_name: str = "node1",
            node_addr: str = "0.0.0.0",
            node_port: int = 4000,
            config_file_path: str = "config.json"
    ) -> None:

        self.node_addr = node_addr
        self._config_data = self._read_config_file(config_file_path)
        self._nodes: list[dict] = self._config_data["nodes"]
        self._tcp_socket: Socket

        self._create_server_socket(node_name, node_addr, node_port)

        self._client_sockets: list[Socket] = []
        self._create_client_sockets(self._nodes)

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
        server_thread = Thread(target=udp_server_thread, args=(self._server_socket,))
        server_thread.start()

        self._tcp_socket = Socket(node_name, AF_INET, SOCK_STREAM)
        self._tcp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._tcp_socket.bind((node_addr, node_port))
        tcp_server_thread = Thread(target=tcp_server_thread_function, args=(self._tcp_socket, self))
        tcp_server_thread.start()

    def _create_client_sockets(self, client_nodes_data: list[dict]) -> None:
        for node_data in client_nodes_data:
            node_name = node_data["node_name"]
            node_addr = node_data["node_addr"]
            node_port = node_data["node_port"]

            if node_name == self._server_socket.name:
                continue

            client_socket = Socket(node_name, AF_INET, SOCK_STREAM)
            self._client_sockets.append(client_socket)
            # client_socket.connect((node_addr, node_port))
            # TODO: wywołanie connect z node_addr i node_port

    def available_files(self) -> list[str]:
        rest_resources = BroadcastMessage("127.0.0.1:4200", self.downloaded_files())
        print(rest_resources.node_addr)
        print(rest_resources.resources)
        # TODO: pobieranie dostępnych plików z innych węzłów (UDP)
        ...

    def downloaded_files(self) -> list[str]:
        return [
            file_name for file_name in os.listdir("./node_data/")
            if file_name != ".gitkeep"
        ]

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
        DATA = BroadcastMessage(self.node_addr, self.downloaded_files())
        for node in self._nodes:
            pb = pickle.dumps(DATA)
            print(node["node_addr"])
            print(node["node_port"])
            self._server_socket.sendto(pb, (node["node_addr"], node["node_port"]))
        # TODO: przekazanie informacji o wgranym pliku innym węzłom
        ...

    def download_file(self, file_name: str, node_name: str) -> None:
        request = DownloadRequest(file_name)
        print(request.filename)

        address = "192.168.1.180"

        # TODO: sprawdzenie czy plik istnieje,
        #       jeśli tak to pobranie go (nie UDP)
        ...

    # def _list_nodes_with_file(self, file_name: str) -> list[str]:
        

    def download_progress(self) -> float:
        # TODO: progres pobierania pliku - float w zkaresie od 0 do 1
        ...
