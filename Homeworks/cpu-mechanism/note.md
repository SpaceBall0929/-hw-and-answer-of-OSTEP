#### Measure the costs of a system call

> 关于read：[(110条消息) Linux C高级编程——文件操作之系统调用_a1314521531的博客-CSDN博客](https://blog.csdn.net/wqx521/article/details/50929735?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_utm_term~default-1-50929735-blog-126620960.pc_relevant_3mothn_strategy_recovery&spm=1001.2101.3001.4242.2&utm_relevant_index=4)

2000000次计算出来的时间差比较稳定，因此选1000000次。

```cpp
#include<iostream>
using namespace std;
#include<sys/time.h>
#include<unistd.h>
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
```

运行10次取平均:

![image-20221122165333402](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221122165333402.png)

舍弃莫名其妙的负值和过高的一项.执行一次syscall的代价大概是0.0753us



#### Measuring the cost of a context

这一问属实没搞明白…然后以后也不想做measure了……

感觉题目表述不太清楚