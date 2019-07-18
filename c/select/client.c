#include<netinet/in.h>
#include<sys/socket.h>
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<sys/select.h>
#include<time.h>
#include<unistd.h>
#include<sys/types.h>
#include<errno.h>

#define MAXLINE     1024
#define IPADDRESS   "127.0.0.1"
#define SERV_PORT   8787

#define max(a, b) (a>b) ? a: b

static void handle_recv_msg(int sockfd, char *buf){
    printf("client recv msg is: %s\n", buf);
    sleep(5);
    write(sockfd, buf, strlen(buf) + 1);
}

static void handle_connection(int sockfd){
    char sendline[MAXLINE], recvline[MAXLINE];
    int maxfdp, stdineof;
    fd_set readfds;
    int n;
    struct timeval tv;
    int retval = 0;

    while(1){
        FD_ZERO(&readfds);
        FD_SET(sockfd, &readfds);
        maxfdp = sockfd;

        tv.tv_sec = 5;
        tv.tv_usec = 0;

        retval = select(maxfdp+1, &readfds, NULL, NULL, &tv);
        if(retval == -1){
            return;
        }

        if(retval == 0){
            printf("client timeout.\n");
            continue;
        }

        if(FD_ISSET(sockfd, &readfds)){
            n = read(sockfd, recvline, MAXLINE);
            if(n<=0){
                fprintf(stderr, "client: server is closed.\n");
                close(sockfd);
                FD_CLR(sockfd, &readfds);
                return;
            }
            handle_recv_msg(sockfd, recvline);
        }
    }
}

int main(int argc, char *argv[]){
    int sockfd;
    struct sockaddr_in servaddr;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    /* 
     * 置字节字符串前n个字节为零且包括‘\0’。也可以将一个结构体清零。
     * 之前在很多地方看到说推荐用memset函数代替bzero函数，原因是在POSIX.1-2001标准里面，
     * 该函数已经被标记为了遗留函数而不推荐使用，前几天我在UNIX网络编程卷一当中看到作者说整本书
     * 都用bzero函数代替memset函数，作者是这样解释的：
     * bzero不是一个ANSI C函数，它起源于早期的Berkeley网络编程代码。
     * 不过我们在整本书中使用它而不使用ANSI C的memset函数，因为bzero（带2个参数）比memset（带3个参数）更好记忆。
     */
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    // 整型变量从主机字节顺序转变成网络字节顺序， 就是整数在地址空间存储方式变为高位字节存放在内存的低地址处。
    servaddr.sin_port = htons(SERV_PORT);
    // inet_pton是一个IP地址转换函数,可以在将IP地址在“点分十进制”和“二进制整数”之间转换
    inet_pton(AF_INET, IPADDRESS, &servaddr.sin_addr);

    int retval = 0;
    retval = connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr));
    if(retval < 0){
        fprintf(stderr, "connect fail, error: %s\n", strerror(errno));
        return -1;
    }
    printf("client send to server.\n");
    write(sockfd, "hello server", 32);

    handle_connection(sockfd);
    return 0;
}