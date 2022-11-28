import socket; HOSTNAME, PORT, MAXDATA = "127.0.0.1", 8081, 1024
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOSTNAME, PORT))
    while "Łukasz": print(s.recvfrom(MAXDATA)[0].decode("utf-8"))
