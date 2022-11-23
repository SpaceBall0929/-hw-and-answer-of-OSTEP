#### Switch the order of the processes: -l 1:0,4:100. What happensnow? Does switching the order matter? Why?

猜测：

|      | p0          | p1      |
| ---- | ----------- | ------- |
|      | run io      | ready   |
|      | block       | run cpu |
|      | block       | run cpu |
|      | block       | run cpu |
|      | block       | run cpu |
|      | block       | done    |
|      | run io_done | done    |

没有错:![image-20221123101022959](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123101022959.png)

和前一次的对比:

![image-20221123101047077](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123101047077.png)

发现应该先运行需要io的程序,这样可以趁着IO的时候运行下一个程序

再观察:

![image-20221123101140992](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123101140992.png)

这个IO还要等后面那个程序运行完后,才能运行io_done(这是因为IO_RUN_IMMEDIATE是打开的)

#### 是否Switch and 是否IO_RUN_immediate

不switch的结果你应该能想到.

来看后一个

这是run_later:

![image-20221123102045356](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123102045356.png)

这是immediate:

![image-20221123102132421](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123102132421.png)

所以感觉IMMEDIATE更好,因为这样的话,让p1马上完成IO,因为如果由下一次IO,此时cpu空闲 就能更好的留给下一个要cpu的进程.

##### 练习题

###### 1

![image-20221123102419865](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123102419865.png)

两个都on

|      | p0          | p1      |
| ---- | ----------- | ------- |
|      | run_cpu     | ready   |
|      | run io      | ready   |
|      | blocked     | run cpu |
|      | blocked     | run cpu |
|      | blocked     | run cpu |
|      | blocked     | done    |
|      | blocked     | done    |
|      | run io_done | done    |
|      | run io      | done    |
|      | blocked     | done    |
|      | blocked     | done    |
|      | blocked     | done    |
|      | blocked     | done    |
|      | blocked     |         |
|      | run io_done |         |

关掉switch

|      | p0          | p1      |
| ---- | ----------- | ------- |
|      | run_cpu     | ready   |
|      | run io      | ready   |
|      | blocked     | ready   |
|      | blocked     | ready   |
|      | blocked     | ready   |
|      | blocked     | ready   |
|      | blocked     | ready   |
|      | run io_done | ready   |
|      | run io      | ready   |
|      | blocked     | ready   |
|      | blocked     | ready   |
|      | blocked     | ready   |
|      | blocked     | ready   |
|      | blocked     | ready   |
|      | run io_done | ready   |
|      | done        | run cpu |
|      | done        | run cpu |
|      | done        | run cpu |

关掉immediate

|      | p0          | p1      |
| ---- | ----------- | ------- |
|      | run_cpu     | ready   |
|      | run io      | ready   |
|      | blocked     | run cpu |
|      | blocked     | run cpu |
|      | blocked     | run cpu |
|      | blocked     | done    |
|      | blocked     | done    |
|      | run io_done | done    |
|      | run io      | done    |
|      | blocked     | done    |
|      | blocked     | done    |
|      | blocked     | done    |
|      | blocked     | done    |
|      | blocked     |         |
|      | run io_done |         |

没区别...

###### 2

![image-20221123103017182](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123103017182.png)

都开:

|      | p0          | p1          | cpu  | IOs  |
| ---- | ----------- | ----------- | ---- | ---- |
|      | run_cpu     | ready       | 1    |      |
|      | run io      | ready       | 1    |      |
|      | blocked     | run io      | 1    | 1    |
|      | blocked     | ready       |      | 1    |
|      | blocked     | ready       |      | 1    |
|      | blocked     | ready       |      | 1    |
|      | blocked     | ready       |      | 1    |
|      | run io_done | ready       | 1    |      |
|      | ready       | run io      | 1    |      |
|      | run cpu     | blocked     | 1    | 1    |
|      | done        | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | run io_done | 1    |      |
|      |             | run io      | 1    |      |
|      |             | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | run io_done | 1    |      |

不对呢^-^原来IO设备可以同时用多个,它是复数...

更正一下:

|      | p0          | p1          | cpu  | IOs  |
| ---- | ----------- | ----------- | ---- | ---- |
|      | run cpu     | ready       | 1    |      |
|      | run io      | ready       | 1    |      |
|      | blocked     | run io      | 1    | 1    |
|      | blocked     | blocked     |      | 2    |
|      | blocked     | blocked     |      | 2    |
|      | blocked     | blocked     |      | 2    |
|      | blocked     | blocked     |      | 2    |
|      | run io_done | blocked     | 1    | 1    |
| !    | ready       | run io_done | 1    |      |
| !    | ready       | run io      | 1    |      |
| !    | run cpu     | blocked     | 1    | 1    |
|      | done        | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | run io_done | 1    |      |
|      |             | run cpu     | 1    |      |
|      |             |             |      |      |

注意看!的部分,因为immediate打开,所以刚IO完的进程cpu会优先执行

,直到这个进程:

1. done
2. blocked
3. 另一个程序IO结束

才会切换.

答案是对的:

![image-20221123104118394](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123104118394.png)

如果把immediate关了:

|      | p0          | p1          | cpu  | IOs  |
| ---- | ----------- | ----------- | ---- | ---- |
|      | run cpu     | ready       | 1    |      |
|      | run io      | ready       | 1    |      |
|      | blocked     | run io      | 1    | 1    |
|      | blocked     | blocked     |      | 2    |
|      | blocked     | blocked     |      | 2    |
|      | blocked     | blocked     |      | 2    |
|      | blocked     | blocked     |      | 2    |
|      | run io_done | blocked     | 1    | 1    |
| !    | run cpu     | ready       | 1    |      |
| !    | done        | run io_done | 1    |      |
| !    |             | run io      | 1    |      |
|      |             | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | blocked     |      | 1    |
|      |             | run io_done | 1    |      |
|      |             | run cpu     |      |      |
