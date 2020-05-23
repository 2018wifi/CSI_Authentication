#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <string.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <stdlib.h>

#define PORT 5500
#define BUF_LEN 1024
#define PC_PORT 3600
char PC_IP[20] = "192.168.1.100";
char buf[BUF_LEN];

int server_fd, raspb;
struct sockaddr_in server_addr;
socklen_t len;
struct sockaddr_in client_addr;  
int server_fd2, ret2;
struct sockaddr_in reciever_addr;

void recieve_udp_and_send_tcp(){
	while(1){
		memset(buf, 0, BUF_LEN);
		int count;
		count = recvfrom(server_fd, buf, BUF_LEN, 0, (struct sockaddr*)&client_addr, &len);
		if (count == -1) {
			perror("recvfrom");
			exit(1);
		}
		printf("get a udp package!\n");
		
		int count2;
		count2 = send(server_fd2, buf, BUF_LEN, 0);
		if (count2 < 0) {
			perror("Send tcp-package imformation");
			exit(1);
		}
		printf("send success!\n");
	}
}

int main() {
	printf("Listening...\n");
	server_fd = socket(AF_INET, SOCK_DGRAM, 0);
	if (server_fd < 0) {
		perror("socket");
		exit(1);
	}
	memset(&server_addr, 0, sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.s_addr = inet_addr("255.255.255.255");
	server_addr.sin_port = htons(PORT);
	int opt = 1;
	setsockopt(server_fd,SOL_SOCKET,SO_REUSEADDR,&opt,sizeof(&opt));
	raspb = bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr));
	if (raspb < 0) {
		perror("bind");
		exit(1);
	}
	
	server_fd2 = socket(AF_INET, SOCK_STREAM, 0);
	if (server_fd2 < 0) {
		perror("socket");
		exit(1);
	}
	memset(&reciever_addr, 0, sizeof(reciever_addr));
	reciever_addr.sin_family = AF_INET;
	reciever_addr.sin_addr.s_addr = inet_addr(PC_IP);
	reciever_addr.sin_port = htons(PC_PORT);
	len = sizeof(client_addr);
	if (connect(server_fd2, (struct sockaddr*)&reciever_addr, sizeof(reciever_addr)) < 0)
	{
		perror("connect");
		exit(1);
	}
		printf("connect success!\n");
	
	recieve_udp_and_send_tcp();
	shutdown(server_fd, 0);
	shutdown(server_fd2, 1);
	return 0;
}
