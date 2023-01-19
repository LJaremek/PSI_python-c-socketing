from __future__ import annotations

from threading import Thread
import pickle
from socket import SO_BROADCAST, SOL_SOCKET, SO_REUSEADDR
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
from socket import socket
import json
import os
import shutil

from datatypes import DownloadRequest, BroadcastMessage, DownloadResponse

IS_UDP_THREAD_RUNNING = True
IS_UPD_RECEVING = True

CHUNK_SIZE = 1024


def udp_server_thread(udp_socket: Socket, node: Node) -> None:
    global IS_UDP_THREAD_RUNNING
    while IS_UDP_THREAD_RUNNING:
        file_names: list[str] = []
        data_bytes = b""
        while IS_UPD_RECEVING:
            chunk, _ = udp_socket.recvfrom(CHUNK_SIZE)
            data_bytes += chunk
            if len(chunk) < CHUNK_SIZE:
                break

        data: BroadcastMessage = pickle.loads(data_bytes)
        if any(x.node_addr == data.node_addr for x in node.available_files):
            for x in node.available_files:
                if x.node_addr == data.node_addr:
                    x.resources = data.resources
        else:
            node.available_files.append(
                BroadcastMessage(
                    data.node_addr,
                    data.node_port,
                    data.resources
                    )
                )

        for file in node.available_files:
            file_names.extend(file.resources)
        node.available_file_names = list(dict.fromkeys(file_names))


def tcp_server_thread_function(tcp_socket: Socket, node: Node) -> None:
    while True:
        tcp_socket.listen()
        conn, _ = tcp_socket.accept()
        data = conn.recv(CHUNK_SIZE)
        request: DownloadRequest = pickle.loads(data)
        filename = request.filename
        if filename not in node.downloaded_files():
            response = None

            for file in node.available_files:
                if filename in file.resources:
                    response = DownloadResponse(
                        False,
                        file.node_addr,
                        file.node_port
                        )

            if not response:
                response = DownloadResponse(False, "", None)
            conn.sendall(pickle.dumps(response))

        else:
            response = DownloadResponse(True, node.node_addr, node.node_port)
            conn.sendall(pickle.dumps(response))
            with open(f"node_data/{filename}", "rb") as f:
                for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
                    conn.sendall(chunk)

        conn.close()


def tcp_client_thread_function(
        client_socket: Socket,
        file_name: str,
        node: Node
        ) -> None:

    with open(f"./node_data/{file_name}", "wb") as f:
        while True:
            data = client_socket.recv(CHUNK_SIZE)
            if not data:
                break
            f.write(data)

    node._file_during_download = ""
    client_socket.close()

    data = BroadcastMessage(
        node.node_addr,
        node.node_port,
        node.downloaded_files()
        )

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
        self.node_port = node_port
        self._config_data = self._read_config_file(config_file_path)
        self._nodes: list[dict] = self._config_data["nodes"]
        self._tcp_socket: Socket

        self.udp_thread: Socket = None
        self._create_server_socket(node_name, node_addr, node_port)

        self._client_socket: Socket
        self.available_files: list[BroadcastMessage] = [
            BroadcastMessage(node_addr, node_port, self.downloaded_files())
            ]

        self.available_file_names: list[str] = []
        for file in self.available_files:
            self.available_file_names.extend(file.resources)

        self.available_file_names = list(
            dict.fromkeys(
                self.available_file_names
                )
            )

        self._file_during_download: str = ""
        self._packet_loss: bool = False

    def imitate_packet_loss(self) -> None:
        self._packet_loss = True

    def kill_udp_thread(self) -> None:
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
    ) -> None:

        self._server_socket = Socket(node_name, AF_INET, SOCK_DGRAM)
        self._server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._server_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._server_socket.bind((node_addr, node_port))

        self.udp_thread = Thread(
            target=udp_server_thread,
            args=(self._server_socket, self)
            )

        self.udp_thread.start()

        self._tcp_socket = Socket(node_name, AF_INET, SOCK_STREAM)
        self._tcp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._tcp_socket.bind((node_addr, node_port))

        tcp_server_thread = Thread(
            target=tcp_server_thread_function,
            args=(self._tcp_socket, self)
            )

        tcp_server_thread.start()

    def get_available_files(self) -> list[str]:
        return self.available_file_names

    def downloaded_files(self) -> list[str]:
        return [
            file_name for file_name in os.listdir("./node_data/")
            if file_name != ".gitkeep"
        ]

    def update_file_list(self, data: BroadcastMessage) -> None:
        if not self._packet_loss:
            pb = pickle.dumps(data)

            chunks = [
                pb[i:i+CHUNK_SIZE]
                for i in range(0, len(pb), CHUNK_SIZE)
                ]

            for node in self._nodes:
                for chunk in chunks:
                    self._server_socket.sendto(
                        chunk,
                        (node["node_addr"], node["node_port"])
                    )

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
        data = BroadcastMessage(
            self.node_addr,
            self.node_port,
            self.downloaded_files()
            )

        self.update_file_list(data)

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

    def choose_node_to_download_from(self, file_name: str) -> None:
        if self._file_during_download != "":
            msg = f"File {self._file_during_download}"
            msg += " is being downloaded right now"
            print(msg)
            return

        if file_name in self.downloaded_files():
            print("File already exists")
            return

        if file_name not in self.available_file_names:
            print("File does not exist")
            return

        print("Available file owners:")
        for name in self._list_file_owners(file_name):
            print(f"-> {name}")

        is_correct_name = False
        while not is_correct_name:
            node_name = input("Choose node to download from: ")
            if node_name not in self._list_file_owners(file_name):
                print("Wrong node name")
            else:
                is_correct_name = True

        for node in self._nodes:
            if node["node_name"] == node_name:
                node_addr = node["node_addr"]
                node_port = node["node_port"]
                return node_name, node_addr, node_port

    def download_file(
            self,
            file_name: str,
            node_name: str,
            node_addr: str,
            node_port: int
            ) -> None:

        request = DownloadRequest(file_name)

        client_socket = Socket(node_name, AF_INET, SOCK_STREAM)
        client_socket.connect((node_addr, node_port))
        client_socket.sendall(pickle.dumps(request))
        data: DownloadResponse = pickle.loads(client_socket.recv(256))

        if data.is_available:
            self._file_during_download = file_name

            tcp_server_thread = Thread(
                target=tcp_client_thread_function,
                args=(client_socket, file_name, self)
                )

            tcp_server_thread.start()

        elif data.node_addr:
            self.download_file(
                file_name,
                node_name,
                data.node_addr,
                data.node_port
                )

        else:
            print("This file is not available")

    def download_progress(self, file_name: str) -> str:
        if (
            file_name != self._file_during_download and
            file_name not in self.downloaded_files()
        ):
            return "File is not being downloaded"

        if file_name in self.downloaded_files():
            return "File is already downloaded"

        return "File is being downloaded"
