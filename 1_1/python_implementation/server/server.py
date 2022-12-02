import socket
import sys

HOSTNAME, MAXDATA = "0.0.0.0", 1024


def main(argc, argv):
    if (argc < 2):
        print(f"Usage: {argv[0]} <PORT>")
        exit(1)
    port = int(argv[1])
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOSTNAME, port))
        while True:
            print(f"Python server received : {s.recvfrom(MAXDATA)[0].decode('utf-8')}")


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
