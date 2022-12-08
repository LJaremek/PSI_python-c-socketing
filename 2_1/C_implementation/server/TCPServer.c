#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>

#define MAXDATA 1024

int isWorking() {
    return 1;
}


int main(int argc, char **argv) {

    // initialize variables
    int sock, conn, bytesRead;
    char buffer[MAXDATA];
    struct sockaddr_in servaddr;

    // get initial arguments
    if (argc < 2) {
        printf("Usage: %s <PORT>\n", argv[0]);
        return 1;
    }
    int port = atoi(argv[1]);

    // create socket
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        perror("Socket creation failed");
        exit(1);
    }

    // config address struct
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(port);

    // bind socket with address structure
    if (bind(sock, (const struct sockaddr *) &servaddr, sizeof(servaddr)) == -1) {
        perror("Opening stream socket failed");
        exit(1);
    }

    // start listening
    if (listen(sock, 5) == -1) {
        perror("Listening initialize failed");
        exit(1);
    }

    // server should work till user interrupts it
    while (isWorking()) {

        // accept connection from client
        conn = accept(sock, (struct sockaddr *) 0, 0);
        if (conn == -1) {
            perror("Accept failed");
            exit(3);
        } else

            // read until there are bytes to read
            do {
                // prepare buffer for data receiving
                memset(buffer, 0, sizeof buffer);

                // read data
                if ((bytesRead = read(conn, buffer, MAXDATA)) == -1) {
                    perror("Reading message failed");
                    exit(4);
                }
                if (bytesRead == 0) {
                    printf("Connection ended \n");
                } else {
                    printf("C server received : %s\n", buffer);
                }
            } while (bytesRead > 0);

        // close connection after receiving data
        close(conn);
    }

}
