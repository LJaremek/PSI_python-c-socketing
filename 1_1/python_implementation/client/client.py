import socket

HOSTNAME, PORT, MAXDATA = "172.21.14.2", 8081, 1024 # parametryzacja
DATA = "hello from python client"


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        for _ in range(5):
            s.sendto(str.encode(DATA, "utf-8"), (HOSTNAME, PORT))
            print(f"Client sent : {DATA}")


if __name__ == "__main__":
    main()
