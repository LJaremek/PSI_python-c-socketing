FROM gcc:4.9
ADD TCPServer.c /
RUN gcc -std=c11 -o TCPServer TCPServer.c
ENTRYPOINT ["./TCPServer"]
