import multiprocessing
import random
import time,os

#发送消息的进程
def proc_send(pipe,urls):
    for url in urls:
        print('Process (%s) send:%s'%(os.getpid(),url))
        pipe.send(url)
        time.sleep(random.random())

#接受消息的进程，由于里面是一个死循环，使用terminate强制结束
def proc_recv(pipe):
    while True:
        print('Process (%s) rev:%s'%(os.getpid(),pipe.recv()))
        time.sleep(random.random())

if __name__ == "__main__":
    #创建pipe通信管道
    pipe = multiprocessing.Pipe()
    #创建Process并执行传递参数，使用了列表生成式
    p1 = multiprocessing.Process(target = proc_send,args = (pipe[0],['url_' + str(i) for i in range(10)]))
    p2 = multiprocessing.Process(target = proc_recv,args = (pipe[1],))

    #启动进程
    p1.start()
    p2.start()
    #实现进程间同步
    p1.join()
    #强制结束进程
    p2.terminate()