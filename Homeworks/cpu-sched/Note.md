##### 1

**SJF**

![image-20221123164730219](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123164730219.png)

|      | turnaround | response |
| ---- | ---------- | -------- |
| 0    | 2          | 0        |
| 1    | 7          | 2        |
| 2    | 15         | 7        |

**RR**

(这个略有点tricky)

![image-20221123165037004](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123165037004.png)



到300s时，三个p各自完成了100，但由于1已经完成，所以只剩两个进程了

|      | turnaround | response | wait            |
| ---- | ---------- | -------- | --------------- |
| 0    | 298        | 0        | 298 - 100 = 198 |
| 1    | 499        | 1        | 499 - 200 = 299 |
| 2    | 600        | 2        | 600 - 300 = 300 |

wait time就是现在的时间减去它需要的时间，就是它空闲的总时间了。

![image-20221123165914078](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123165914078.png)



##### For what types of workloads and quantum lengths does SJF deliver the same response times as RR?

quantum lengths >=max项目长度的时候

##### What happens to response time with SJF as job lengths increase? Can you use the simulator to demonstrate the trend?

这要看是谁increase了，

1. 如果是最长的那个项目，那么完全没变化，

   ![image-20221123170538795](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123170538795.png)

2. 如果是最短的项目，且变完还是最短的，那么除了第一个，所有response time都增加$\Delta t$![image-20221123170620197](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123170620197.png)

   

3. 如果在中间：

   - 加完排列不变，那么它后面的都增加$\Delta t$![image-20221123170713111](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123170713111.png)
   - 加完排序变了，那么前进的任务都减少了这个任务的执行时间，这个任务增加了前进的所有任务的执行时间之和，后面的任务都增加$\Delta t$![image-20221123170842359](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123170842359.png)![image-20221123171003590](https://camillle-img.oss-cn-hangzhou.aliyuncs.com/img/image-20221123171003590.png)

##### What happens to response time with RR as quantum lengths increase? Can you write an equation that gives the worst-case response time, given N jobs?

大于等于所有项目最大值的时候