from multiprocessing import Pipe
from os import fork, getpid, pipe, wait, waitpid
import sys
from time import sleep
def change_var():
    x = 100
    f = fork()
    if f < 0:
        print("fork failed")
    elif f == 0:
        print(f"I'm child,x = {x}")
        x += 1
        print(f"I'm child,change x to {x}")
    else:
        wait()
        print(f"I'm parent,x = {x}")
        x += 3
        print(f"I'm parent,change x to {x}")

def open_file():
    f = open('test.txt','w')
    i = fork()
    if i < 0:
        print("fork failed")
    elif i == 0:
        fvar = id(f)
        print(f"I'm child and f = {fvar}")
        f.write("write by child")
    else:
        fvar = id(f)
        print(f"I'm parent and f = {fvar}")
        f.write("write by parent")
    f.close()

def open_file2():
    i = fork()
    if i < 0:
        print("fork failed")
    elif i == 0:
        f = open('test.txt','w')
        fvar = id(f)
        print(f"I'm child and f = {fvar}")
        f.write("write by child")
    else:
        wait()
        f = open('test.txt','w')
        fvar = id(f)
        print(f"I'm parent and f = {fvar}")
        f.write("write by parent")
    f.close()

def greet():
    """让子进程先输出hello，父进程输出goodbye
        这里使用的方法是定义一个tag
    """
    """i = fork()
    tag = 1
    if i < 0:
        print("fork failed")
    elif i == 0:
        print("Hello")
        tag -= 1
        print(tag)
    else:
        print(tag)
        if tag < 1:
            print("Goodbye")
        print(tag)"""
    
    #不行，因为如果父进程执行完了也就结束了，无论是否判断tag……
    #因此用sleep，让父亲睡久一点……
    i = fork()
    if i < 0:
        print("fork failed")
    elif i == 0:
        print("Hello")
    else:
        sleep(1)
        print("Goodbye")
        #完美解决

def try_exec():
    """尝试各种exec函数
        参考:http://t.csdn.cn/Rar7O
        http://t.csdn.cn/osmBY
        把鼠标放到exec上，点开链接可以看到更多info
    """
    i = fork()
    if i < 0:
        print("fork failed")
    elif i == 0:
        print("I'm the child")
        f = open("yeah.py")
        s = f.read()
        f.close()
        exec(s)
    else:
        print("I'm the parent")

def wait_return():
    """可知wait返回(子进程的pid, 是否成功的status)
    """
    i = fork()
    if i < 0:
        print("fork failed")
    elif i == 0:
        pid = getpid()
        print(f"I'm the child and pid is {pid}")
    else:
        w = wait()
        pid = getpid()
        print(f"I'm the parent, pid is {pid} and wait() return {w}")

def waitpid_return():
    """http://t.csdn.cn/JcmeS
与wait相比就是可以指定子进程了
    """
    i = fork()
    if i < 0:
        print("fork failed")
    elif i == 0:
        pid = getpid()
        print(f"I'm the child and pid is {pid}")
        
    else:
        i2 = fork()
        if i2 == 0:
            pid = getpid()
            print(f"I'm the second child and pid is {pid}")
        pid = getpid()
        w = waitpid(pid + 2, 0)
        print(f"I'm the parent, pid is {pid} and wait() return {w}")
        
def print_after_close():
    """重定向stdout之后会print到文件里
    """
    i = fork()
    if i < 0:
        print("fork failed")
    elif i == 0:
        pid = getpid()
        print(f"I'm the child and pid is {pid}")
        sys.stdout = open("yeah.py",'w')
        print("test")
    else:
        pid = getpid()
        print(f"I'm the parent, pid is {pid}")

def pipe_():
    """参考：http://t.csdn.cn/oPWzu
    注意要wait一下
    pipe的两个返回值：第一个是用来送东西的进口，用send()送东西；
                     第二个是拿东西的出口，用recv来读
                     如果传参是true，那两边都可以进出
    """
    fd1, fd2 = Pipe()
    i = fork()
    if i < 0:
        print("fork failed")
    elif i == 0:
        pid = getpid()
        print(f"I'm the child and pid is {pid},please input:")
        msg = input()
        fd1.send(msg)
        
    else:
        wait()
        i2 = fork()
        if i2 == 0:
            pid = getpid()
            print(f"I'm the second child and pid is {pid}")
            print(fd2.recv())
            return
        pid = getpid()
        print(f"I'm the parent, pid is {pid}")

pipe_()