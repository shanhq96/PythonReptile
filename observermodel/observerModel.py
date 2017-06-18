# encoding=utf-8
"""
__author__ = 'shanhq96@gmail.com'
"""
from abc import ABCMeta, abstractmethod


class Subject():
    """抽象主题/通知者"""
    __metaclass__ = ABCMeta
    observers = []
    status = ''

    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass


class Observer():
    """抽象观察者"""
    __metaclass__ = ABCMeta

    def __init__(self, name, sub, connection,collection):
        self.name = name
        self.sub = sub
        self.connection = connection
        self.collection = collection

    @abstractmethod
    def update(self):
        pass


class ListNotifier(Subject):
    """具体主题"""
    __dataList = []  # 拥有一个私有的list 只可以通过内部方法进行维护

    def __init__(self):
        pass

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, dataList2Save):
        for observer in self.observers:
            observer.update(dataList2Save)

    def appendNewData2List(self, newData):
        """插入数据到__dataList中"""
        self.__dataList.append(newData)
        if (len(self.__dataList) >= 20):
            self.status = '数据量达到了', len(self.__dataList)
            temp = self.__dataList[0:20]
            self.__dataList = self.__dataList[20:]
            self.notify(temp)


    def printList(self):
        """打印__dataList"""
        print("当前list中数据:", self.__dataList)


class DbListManage(Observer):
    """具体观察者"""

    def update(self, dataList2Save):
        """将传来的列表存储到数据库中"""
        #print('%s,%s存储了5条数据,数据为%s' % (self.sub.status, self.name, dataList2Save))
        temp = self.connection.insertList(self.collection,dataList2Save)
        return temp

#
# if __name__ == '__main__':
#     dataList = []
#     listNotifier = ListNotifier()
#     observe1 = DbListManage('list存储观察者', listNotifier)
#     listNotifier.attach(observe1)
#     # boss.detach(observe2)
#
#     listNotifier.appendNewData2List(1)
#     listNotifier.appendNewData2List(2)
#     listNotifier.appendNewData2List(3)
#     listNotifier.appendNewData2List(4)
#     listNotifier.appendNewData2List(5)
#     listNotifier.appendNewData2List(6)
#     listNotifier.appendNewData2List(7)
#     listNotifier.appendNewData2List(8)
#     listNotifier.appendNewData2List(9)
#     listNotifier.appendNewData2List(10)
#     listNotifier.appendNewData2List(11)
#
#     # listNotifier.status = 'list中多了5条数据'
#     # listNotifier.notify()
#     listNotifier.printList()
