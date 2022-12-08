import socket
import sys

HOSTNAME, MAXDATA = "0.0.0.0", 1024


def is_working():
    return True


def main(argc, argv):
    # get inital arguments
    if (argc < 2):
        print(f"Usage: {argv[0]} <PORT>")
        exit(1)
    port = int(argv[1])

    # create stream socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # bind socket to hostname and port
        s.bind((HOSTNAME, port))

        # start listening
        s.listen(5)

        # server should work till user interrupts it
        while is_working():

            # accept connection from client
            conn, addr = s.accept()
            with conn:

                # receive data from client
                data = conn.recv(MAXDATA)
                if not data:
                    break
                print(f"Python server received : {data.decode('utf-8')}")

            # close connection after receiving data
            conn.close()


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
