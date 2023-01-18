class DownloadRequest(object):
    def __init__(self, filename: str):
        self.filename = filename


class DownloadResponse(object):
    def __init__(self, is_available: bool, node_addr: str):
        self.is_available = is_available
        self.node_addr = node_addr


class BroadcastMessage(object):
    def __init__(self, node_addr: str, resources: list[str]):
        self.node_addr = node_addr
        self.resources = resources
