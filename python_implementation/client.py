import socket

HOSTNAME, PORT, MAXDATA = "127.0.0.1", 8081, 1024
DATA = "hello from python client"


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        for _ in range(5):
            s.sendto(str.encode(DATA, "utf-8"), (HOSTNAME, PORT))


if __name__ == "__main__":
    main()
