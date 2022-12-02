import socket
import struct
import io

HOSTNAME, PORT, MAXDATA = "0.0.0.0", 8081, 1024 # parametryzacja portu

NETWORK_BYTE_ORDER = "!"
PADDING = "4x"
STRING = "10s"
LONG = "l"
SHORT = "h"
FORMAT = NETWORK_BYTE_ORDER + LONG + PADDING + SHORT + STRING + PADDING


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOSTNAME, PORT))
        while True:
            data = s.recvfrom(MAXDATA)
            long, short, string = struct.unpack(FORMAT, data[0])
            print(f"Python server received :\tlong: {long}, short: {short}, string: {string}")


if __name__ == "__main__":
    main()
