import socket
import sys

MAXDATA = 1024
DATA = "hello from python client"


def main(argc, argv):
    if argc < 3:
        print(f"Usage: {argv[0]} <HOSTNAME> <PORT>")
        exit(1)
    hostname = argv[1]
    port = int(argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((hostname, port))
        s.sendto(DATA.encode('utf-8'), (hostname, port))


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
