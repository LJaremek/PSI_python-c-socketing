class DownloadRequest(object):
    def __init__(self, filename: str) -> None:
        self.filename: str = filename


class DownloadResponse(object):
    def __init__(
            self,
            is_available: bool,
            node_addr: str,
            node_port: int
            ) -> None:

        self.is_available: bool = is_available
        self.node_addr: str = node_addr
        self.node_port: int = node_port


class BroadcastMessage(object):
    def __init__(
            self,
            node_addr: str,
            node_port: int,
            resources: list[str]
            ) -> None:

        self.node_addr: str = node_addr
        self.node_port: int = node_port
        self.resources: list[str] = resources
