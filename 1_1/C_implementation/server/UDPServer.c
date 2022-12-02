#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define MAXDATA 1024


int main(int argc, char** argv) {
    int sock, len;
    char buffer[MAXDATA];
    struct sockaddr_in servaddr, cliaddr;

    if (argc < 2) {
        printf("Usage: %s <PORT>\n", argv[0]);
        return 1;
    }
    int port = atoi(argv[1]);

    sock = socket(AF_INET, SOCK_DGRAM, 0);
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

    len = sizeof(cliaddr);

    while (1) {
        int received = recvfrom(sock, (char *) buffer, MAXDATA, 0, (struct sockaddr *) &cliaddr, &len);
        buffer[received] = '\0';
        printf("C server received : %s\n", buffer);
    }

}
