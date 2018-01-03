#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include<string.h>

// TCP Client
 
int main(int argc,char **argv)
{
    int sock_fd,n;
    char sendline[100];
    char recvline[100];
    struct sockaddr_in servaddr;
 
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    bzero( &servaddr, sizeof(servaddr));
 
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(8080);
 
    inet_pton(AF_INET,"10.10.1.100", &(servaddr.sin_addr));
 
    connect(sock_fd, (struct sockaddr *) &servaddr, sizeof(servaddr));
 
    while(1)
    {
        bzero( sendline, 100);
        bzero( recvline, 100);
        fgets(sendline,100,stdin); /*stdin = 0 , for standard input */
 
        write(sock_fd,sendline,strlen(sendline)+1);
        read(sock_fd,recvline,100);
        printf("%s",recvline);
    }
 
}
