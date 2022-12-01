FROM gcc:4.9
ADD UDPServer.c /
RUN gcc -std=c11 -o UDPServer UDPServer.c
ENTRYPOINT ["./UDPServer"]
