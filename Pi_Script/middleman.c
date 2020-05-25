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
char PC_IP[20] = "192.168.0.100";
int PC_PORT;
char buf[BUF_LEN];
int dst_count;

int server_fd, raspb;
struct sockaddr_in server_addr;
socklen_t len;
struct sockaddr_in client_addr;  
int server_fd2, ret2;
struct sockaddr_in receiver_addr;

void receive_udp_send_udp(){
	int count = 0;
	int udp_len = 0;
	while(1){
		memset(buf, 0, BUF_LEN);
		udp_len = recvfrom(server_fd, buf, BUF_LEN, 0, (struct sockaddr*)&client_addr, &len);
		if (udp_len == -1) {
			perror("Error: recv from nexmon");
			exit(1);
		}
		count += 1;
		printf("%d\tRecv udp from nexmon\n", count);
		
		sendto(server_fd2, buf, udp_len, 0, (struct sockaddr *)&receiver_addr, sizeof(receiver_addr));
		printf("%d\tSend to PC %s\tlen: %d\n", count, PC_IP, udp_len);
	}
}

int main(int argc, char *argv[]) {
	printf("Initiating...\n");
    PC_PORT = atoi(argv[1]);
    dst_count = atoi(argv[2]);
	server_fd = socket(AF_INET, SOCK_DGRAM, 0);
	if (server_fd < 0) {
		perror("Error: server_fd");
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
		perror("Error: bind raspb");
		exit(1);
	}
	
	server_fd2 = socket(AF_INET, SOCK_DGRAM, 0);
	if (server_fd2 < 0) {
		perror("Error: server_fd2");
		exit(1);
	}
	memset(&receiver_addr, 0, sizeof(receiver_addr));
	receiver_addr.sin_family = AF_INET;
	receiver_addr.sin_addr.s_addr = inet_addr(PC_IP);
	receiver_addr.sin_port = htons(PC_PORT);
	
	receive_udp_send_udp();
	shutdown(server_fd, 0);
	shutdown(server_fd2, 1);
	return 0;
}
