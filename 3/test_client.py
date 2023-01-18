import pickle
import socket
import sys

HOSTNAME, MAXDATA = "127.0.0.1", 1024


def main(argc, argv):
    port = 4200
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOSTNAME, port))
        while True:
            data = pickle.loads(s.recv(MAXDATA))
            print(f"Python server received : {data.node_addr} {data.resources}")


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
