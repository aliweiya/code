/*
 * 惊群效应演示
 * 通过telnet连接
 */
#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<sys/wait.h>
#include<string.h>
#include<netinet/in.h>
#include<unistd.h>

#define PROCESS_NUM 10
int main(){
    int fd = socket(AF_INET, SOCK_STREAM, 0)
    int connfd;
    int pid;

    char sendbuff[1024];
    struct sockaddr_in serveraddr;
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_port = htons(1234);
    bind(fd, (struct sockaddr *)&serveraddr, sizeof(serveraddr));
    listen(fd, 1024);
    int i;
    for(i=0; i<PROCESS_NUM; ++i){
        pid = fork();
        if(pid == 0){
            while(1){
                connfd = accept(fd, (struct sockaddr*)NULL, NULL);
                if(connfd == 0){
                    sprintf(sendbuff, sizeof(sendbuff), "接收到accept事件的进程PID = %d\n", getpid());
                    send(connfd, sendbuff, strlen(sendbuff)+1, 0);
                    printf("process %d accept success\n", getpid());
                    close(connfd);
                }
                else{
                    printf("process %d accept a connection failed: %s\n", getpid(), strerror(e));
                    close(connfd);
                }
            }
        }
    }
    wait(0);
    return 0;
}