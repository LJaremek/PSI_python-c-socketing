import socket
import struct
import sys

HOSTNAME, MAXDATA = "0.0.0.0", 1024

NETWORK_BYTE_ORDER = "!"
PADDING = "4x"
STRING = "10s"
LONG = "l"
SHORT = "h"
FORMAT = NETWORK_BYTE_ORDER + LONG + PADDING + SHORT + STRING + PADDING


def main(argc, argv):
    if (argc < 2):
        print(f"Usage: {argv[0]} <PORT>")
        exit(1)
    port = int(argv[1])
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOSTNAME, port))
        while True:
            data = s.recvfrom(MAXDATA)
            long, short, string = struct.unpack(FORMAT, data[0])
            print(f"Python server received :\tlong: {long}, short: {short}, string: {string}")


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
