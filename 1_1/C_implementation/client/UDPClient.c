#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#define DATA "hello from C client"
#define HOSTNAME "127.0.0.1" // parametryzacja

int main() {
    int sock;
    struct sockaddr_in cliaddr;
    struct hostent *hp;

    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        perror("opening datagram socket failed");
        exit(1);
    }
    hp = gethostbyname(HOSTNAME);
    if (hp == (struct hostent *) 0) {
        fprintf(stderr, "%s: unknown host\n", HOSTNAME);
        exit(2);
    }
    memcpy((char *) &cliaddr.sin_addr, (char *) hp->h_addr,
           hp->h_length);

    cliaddr.sin_family = AF_INET;
    cliaddr.sin_port = htons(8081);

    for (int i = 0; i < 5; i++) {
        if (sendto(sock, (const char *) DATA, strlen(DATA), MSG_CONFIRM, (const struct sockaddr *) &cliaddr,
                   sizeof(cliaddr)) == -1) {
            perror("sending datagram message failed");
        }
		else {
			printf("Client sent : %s\n", DATA);
		}
    }
    close(sock);
    return 0;
}
