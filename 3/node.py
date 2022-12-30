from socket import socket
import json
import os


class Node:
    def __init__(self, config_file_path: str = "config.json") -> None:
        self._config_data = self._read_config_file(config_file_path)
        self._nodes: list[dict] = self._config_data["nodes"]

    def _read_config_file(self, config_file_path: str) -> list[dict]:
        with open(config_file_path, "r", -1, "utf-8") as f:
            return json.load(f)

    def _create_socket(
            self,
            node_name: str,
            node_addr: str,
            node_port: str
            ) -> socket:
        # TODO: gniazda xd
        ...

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
