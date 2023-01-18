from cmd import Cmd

from node import Node


class P2PShell(Cmd):
    prompt = '> '
    intro = "Welcome! Type ? to list commands"
    node = Node("Radkoski", "192.168.1.115", 4200)

    def do_downloaded_files(self, arg):
        for file in self.node.downloaded_files():
            print(file)

    def help_downloaded_files(self):
        print("List all files located in local node")

    def do_available_files(self, arg):
        print(self.node.available_files())

    def help_available_files(self):
        print("List all files located in all nodes")

    def do_download_file(self, arg):
        if arg == '':
            print("Please provide file name")
            return
        self.node.download_file(arg)

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
        print(arg)
        print("Downloading progress")

    def help_download_progress(self):
        print("Download progress")

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
