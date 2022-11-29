import socket
import struct
import io

HOSTNAME, PORT, MAXDATA = "127.0.0.1", 8081, 1024


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOSTNAME, PORT))
        while True:
            data = s.recvfrom(MAXDATA)
            result = struct.unpack("!l4xh10s4x", data[0])
            print(result)


if __name__ == "__main__":
    main()
