#include<iostream>
using namespace std;
#include<sys/time.h>
#include<unistd.h>
#include<sys/file.h>
#define loop 2000000

void test();

int main()
{   
    int fd = open("test.txt", R_OK);
    char str[10];
    struct timeval t_start, t_end;

    gettimeofday(&t_start, NULL);//开始
    for(int i = 0; i < loop; i++){
        read(fd, str, 0);//系统调用
    }
    gettimeofday(&t_end, NULL);//结束时间

    cout<<"The cost is "<<t_end.tv_usec - t_start.tv_usec<<" us"<<endl;
    close(fd);
    return 0;
}

void test(){
    int test;
    test += 1;
}