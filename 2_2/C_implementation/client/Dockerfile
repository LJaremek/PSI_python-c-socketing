FROM gcc:4.9
ADD TCPClient.c /
RUN gcc -std=c11 -o Client TCPClient.c
ENTRYPOINT ["./Client"]
