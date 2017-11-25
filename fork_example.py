'''
Caption:使用os模块中的fork()方法实现多进程
Date:2017-10-12 00:30
Author:威池军博
'''
import os
if __name__ == '__main__':
    #getpid():获得当前进程的ID
    print('current Process (%s) start ...'%(os.getpid()))

    '''
    fork()函数有两个不同的返回值,在子进程中返回0,在父进程中返回子进程的ID
    从调用fork()函数开始由当前进程和创建的子进程共同执行后面的程序，两个进
    程不共享内存空间.
    '''
    pid = os.fork()

    if pid < 0:
        print('error in fork!')
    elif pid == 0:
        #getppid()获得父进程的ID
        print('I am child process (%s) and my parent process is (%s).'%(os.getpid(),os.getppid()))
    else:
        print('I (%s) created a child process (%s).'%(os.getpid(),pid))
