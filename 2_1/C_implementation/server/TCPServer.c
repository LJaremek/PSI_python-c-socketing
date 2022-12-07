#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>

#define MAXDATA 1024


int main(int argc, char **argv) {
    int sock, msgsock, rval;
    char buffer[MAXDATA];
    struct sockaddr_in servaddr;

    if (argc < 2) {
        printf("Usage: %s <PORT>\n", argv[0]);
        return 1;
    }
    int port = atoi(argv[1]);

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        perror("socket creation failed");
        exit(1);
    }

    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(port);

    if (bind(sock, (const struct sockaddr *) &servaddr, sizeof(servaddr)) == -1) {
        perror("binding datagram socket failed");
        exit(1);
    }

    listen(sock, 5);

    do {
        msgsock = accept(sock, (struct sockaddr *) 0, 0);
        if (msgsock == -1) {
            perror("Accept failed");
            exit(3);
        } else
            do {
                memset(buffer, 0, sizeof buffer);
                if ((rval = read(msgsock, buffer, MAXDATA)) == -1) {
                    perror("Reading message failed");
                    exit(4);
                }
                if (rval == 0) {
                    printf("Connection ended \n");
                } else {
                    printf("%s\n", buffer);
                }
            } while (rval > 0);
        close(msgsock);
    } while (1);

}
