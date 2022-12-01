FROM gcc:4.9
ADD client.c /
RUN gcc -std=c11 -o Client client.c
ENTRYPOINT ["./Client"]
