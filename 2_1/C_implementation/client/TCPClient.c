#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#define h_addr h_addr_list[0]

#define DATA "hello from TCP C client"

int main(int argc, char **argv) {
    int sock;
    struct sockaddr_in cliaddr;
    struct hostent *hp;

    if (argc < 3) {
        printf("Usage: %s <HOSTNAME> <PORT>\n", argv[0]);
        return 1;
    }
    char *hostname = argv[1];
    int port = atoi(argv[2]);

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        perror("opening datagram socket failed");
        exit(1);
    }
    hp = gethostbyname(hostname);
    if (hp == (struct hostent *) 0) {
        fprintf(stderr, "%s: unknown host\n", hostname);
        exit(2);
    }
    memcpy((char *) &cliaddr.sin_addr, (char *) hp->h_addr,
           hp->h_length);

    cliaddr.sin_family = AF_INET;
    cliaddr.sin_port = htons(port);

    if (connect(sock, (struct sockaddr *) &cliaddr, sizeof cliaddr)) {
        perror("Connect to server fail");
        exit(1);
    }
    if (write(sock, DATA, sizeof DATA) == -1) perror("Writing failed");

    close(sock);
    return 0;
}
