#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

#define HOSTNAME "127.0.0.1" // parametryzacja

struct test_struct {
    long int a;
    short int b;
    char c[10];
};

void prepare_struct(struct test_struct* ts) {
    ts->a = htonl(ts->a);
    ts->b = htons(ts->b);
}

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

    struct test_struct a;
    a.a = 123456789;
    a.b = 123;
    strcpy(a.c, "Zadanie13");
    prepare_struct(&a);

    if (sendto(sock, &a, sizeof (struct test_struct), MSG_CONFIRM, (const struct sockaddr *) &cliaddr,
        sizeof(cliaddr)) == -1) {
        perror("sending datagram message failed");
    }
	else {
		printf("Client sent struct with string : %s\n", a.c);
	}

    close(sock);
    return 0;
}

