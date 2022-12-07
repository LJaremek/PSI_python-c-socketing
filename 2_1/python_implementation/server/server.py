import socket
import sys

HOSTNAME, MAXDATA = "0.0.0.0", 1024


def main(argc, argv):
    if (argc < 2):
        print(f"Usage: {argv[0]} <PORT>")
        exit(1)
    port = int(argv[1])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOSTNAME, port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(MAXDATA)
                if not data:
                    break
                print(f"Python server received : {data.decode('utf-8')}")
            conn.close()


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
