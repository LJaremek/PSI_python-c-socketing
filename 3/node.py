
from socket import AF_INET, SOCK_STREAM
from socket import socket
import json
import os


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
            node_port: str,
            config_file_path: str = "config.json"
            ) -> None:

        self._config_data = self._read_config_file(config_file_path)
        self._nodes: list[dict] = self._config_data["nodes"]

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
            node_port: str
            ) -> socket:

        self._server_socket = Socket(node_name, AF_INET, SOCK_STREAM)
        self._server_socket.bind((node_addr, node_port))
        self._server_socket.listen(5)
        # TODO: puścić server na Thread

    def _create_client_sockets(self, client_nodes_data: list[dict]) -> None:
        for node_data in client_nodes_data:
            node_name = node_data["node_name"]
            # node_addr = node_data["node_addr"]
            # node_port = node_data["node_port"]

            if node_name == self._server_socket.name:
                continue

            client_socket = Socket(node_name, AF_INET, SOCK_STREAM)
            self._client_sockets.append(client_socket)
            # TODO: wywołanie connect z node_addr i node_port

    def available_files(self) -> list[str]:
        # TODO: pobieranie dostępnych plików z innych węzłów (UDP)
        ...

    def downloaded_files(self) -> list[str]:
        return [
            file_name for file_name in os.listdir("./node_data/")
            if file_name != ".gitkeep"
            ]

    def upload_file(self, file_path: str) -> None:
        # TODO: wgranie pliku do folderu ./node_data/ oraz
        #       przekazanie tej informacji innym węzłom
        ...

    def download_file(self, file_name: str, node_name: str) -> None:
        # TODO: sprawdzenie czy plik istnieje,
        #       jeśli tak to pobranie go (nie UDP)
        ...

    def download_progress(self) -> float:
        # TODO: progres pobierania pliku - float w zkaresie od 0 do 1
        ...

    def upload_progress(self) -> float:
        # TODO: progres wgrywania pliku - float w zkaresie od 0 do 1
        ...
