from observermodel import observerModel
import connectdb
from lianjia import lianjiaReptile, lianjiaReptileSh
from fangtx import fangtxReptile
from anjuke import anjukeReptile
import threading
from datetime import date, time, datetime, timedelta

USER_IN_NUB = 100
WAIT_ONE_PAGE = 5
WAIT_ONE_DATA = 1.5


def lianjiaFunc(listNotifier):
    """链家测试"""
    lianjia = lianjiaReptile.LianjiaReptile(listNotifier,USER_IN_NUB,WAIT_ONE_PAGE,WAIT_ONE_DATA)
    lianjia.main()


def fangtxFunc(listNotifier):
    """房天下测试"""
    fangtx = fangtxReptile.FangtxReptile(listNotifier,USER_IN_NUB,WAIT_ONE_PAGE,WAIT_ONE_DATA)
    fangtx.main()


def anjukeFunc(listNotifier):
    """安居客测试"""
    anjuke = anjukeReptile.AnjukeReptile(listNotifier,USER_IN_NUB,WAIT_ONE_PAGE,WAIT_ONE_DATA)
    anjuke.main()


def main():
    connection = connectdb.ConnectMongoDB()
    rentDataCollection = connection.getCollection('rentdata')
    listNotifier = observerModel.ListNotifier()
    observer = observerModel.DbListManage('list存储观察者', listNotifier, connection, rentDataCollection)
    listNotifier.attach(observer)

    threads = []
    t1 = threading.Thread(target=lianjiaFunc, args=(listNotifier,))
    threads.append(t1)
    t2 = threading.Thread(target=fangtxFunc, args=(listNotifier,))
    threads.append(t2)
    t3 = threading.Thread(target=anjukeFunc, args=(listNotifier,))
    threads.append(t3)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

def runTask(func, day=0, hour=0, min=0, second=0):
    # Init time
    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    print("now:", strnow)
    print("开始爬虫: %s" % strnow)
    # Call task func
    func()
    print("本次爬虫执行结束")
    # First next run time
    period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    print("next run:", strnext_time)

    while True:
        # Get system current time
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) == str(strnext_time):
            # Get every start work time
            print("开始爬虫: %s" % iter_now_time)
            # Call task func
            func()
            print("本次爬虫执行结束")
            # Get next iteration time
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            print("next_iter: %s" % strnext_time)
            # Continue next iteration
            continue


if __name__ == "__main__":
    # main()
    #runTask(main, min=0.5)
    runTask(main, day=1, hour=0, min=0)
