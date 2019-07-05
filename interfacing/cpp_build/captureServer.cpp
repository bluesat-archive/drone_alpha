#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>

// TODO open network socket
// TODO open pipe to ffmpeg
// TODO join network write to ffmpeg read
// TODO convert to opencv readable format
// TODO convert to 

#define PORT 8000
#define ADR "192.168.4.1"

int main (int argc, char **argv) {
    int pipefd[2];
    struct sockaddr_in address;
    int net = socket(AF_INET, SOCK_STREAM, 0);
    pid_t cpid;
    char buf;
    char *ffmpeg[] = {"ffmpeg", "-i", "-", "-pix_fmt", "bgr24",
    "-vcodec", "rawVideo", "-an", "-sn", "-f", "image2pipe", "-"};

    if (net < 0) {
        perror("Unable to connect to socket");
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_port = htons(PORT);

    if (inet_pton(AF_INET, ADR, &address.sin_addr) <= 0) {
        perror("Invalid address");
        exit(EXIT_FAILURE);
    }

    if (connect(net, (struct sockaddr *) &address, sizeof(address)) < 0) {
        perror("Connection failed");
        exit(EXIT_FAILURE);
    }

    cpid = pipe(pipefd);
    if (cpid < 0) {
        exit(EXIT_FAILURE);
    }
    // 0 is input pipe 0 is read for child
    // 1 is output pipe 1 is write of child
    if (cpid == 0) {
        close(0);
        dup(net); // Done // Replace with network pipe
        close(1);
        dup(pipefd[1]);
        cpid = execvp(ffmpeg[0], ffmpeg);
        if (cpid < 0) {
            exit(EXIT_FAILURE);
        }
    }
    else {

    }

    return EXIT_SUCCESS;
}