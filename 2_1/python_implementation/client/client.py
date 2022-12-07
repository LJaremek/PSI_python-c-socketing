import socket
import sys

MAXDATA, DATA = 1024, "hello from python tcp client"


def main(argc, argv):
    # get initial arguments
    if argc < 3:
        print(f"Usage: {argv[0]} <HOSTNAME> <PORT>")
        exit(1)
    hostname = argv[1]
    port = int(argv[2])

    # create stream socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # connect with server
        s.connect((hostname, port))

        # send data to server
        s.sendto(DATA.encode('utf-8'), (hostname, port))


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
