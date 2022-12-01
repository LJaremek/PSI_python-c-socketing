FROM gcc:4.9
ADD UDPClient.c /
RUN gcc -std=c11 -o UDPClient UDPClient.c
ENTRYPOINT ["./UDPClient"]
