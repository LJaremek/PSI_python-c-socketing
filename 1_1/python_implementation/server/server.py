import socket

HOSTNAME, PORT, MAXDATA = "0.0.0.0", 8081, 1024 # parametryzacja portu


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOSTNAME, PORT))
        while True:
            print(f"Python server received : {s.recvfrom(MAXDATA)[0].decode('utf-8')}")


if __name__ == "__main__":
    main()
