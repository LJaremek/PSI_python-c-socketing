import json

from cmd import Cmd

from node import Node


class P2PShell(Cmd):
    prompt = '> '
    intro = "Welcome! Type ? to list commands"
    config_file_path = "node_config.json"
    with open(config_file_path, "r", -1, "utf-8") as f:
        config = json.load(f)
    node = Node(config["node_name"], config["node_addr"], config["node_port"])

    def do_downloaded_files(self, arg) -> None:
        if len(self.node.downloaded_files()) == 0:
            print("No files downloaded")
            return

        print("List of downloaded files:")
        for file in self.node.downloaded_files():
            print(f"-> {file}")

    def help_downloaded_files(self) -> None:
        print("List all files located in local node")

    def do_available_files(self, arg) -> None:
        available_files = self.node.get_available_files()
        if len(available_files) == 0:
            print("No files available")
            return

        print("List of available files:")
        for file in self.node.get_available_files():
            print(f"-> {file}")

    def help_available_files(self) -> None:
        print("List all files located in all nodes")

    def do_download_file(self, arg) -> None:
        if arg == '':
            print("Please provide file name")
            return

        node = self.node.choose_node_to_download_from(arg)
        if not node:
            return

        node_name, node_addr, node_port = node
        self.node.download_file(arg, node_name, node_addr, node_port)

    def help_download_file(self):
        print("Download file from the network")

    def do_upload_file(self, arg):
        if arg == '':
            print("Please provide file name")
            return
        self.node.upload_file(arg)

    def help_upload_file(self):
        print("Upload file to the network")

    def do_download_progress(self, arg):
        if arg == '':
            print("Please provide file name")
            return
        print(self.node.download_progress(arg))

    def help_download_progress(self):
        print("Download progress")

    def do_imitate_packet_loss(self, arg):
        self.node.imitate_packet_loss()

    def help_imitate_packet_loss(self):
        print("Imitate UDP packet loss")

    def do_exit(self, arg):
        print("Bye")
        self.node.kill_udp_thread()
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D.')

    def default(self, arg):
        if arg == 'x' or arg == 'q':
            return self.do_exit(arg)

        print("Default: {}".format(arg))
