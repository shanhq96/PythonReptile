import requests
from lxml import etree
import re
import time
import common


class FangtxReptile():
    """房天下爬虫类"""

    def __init__(self, ListNotifier,USER_IN_NUB,WAIT_ONE_PAGE,WAIT_ONE_DATA, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
                 url='http://zu.sh.fang.com'):
        """初始化连接信息"""
        self.headers = headers
        self.url = url
        req = requests.get(url)
        self.cookie = req.cookies.get_dict()
        self.USER_IN_NUB = USER_IN_NUB  # 爬的页数
        self.WAIT_ONE_PAGE = WAIT_ONE_PAGE  # 每爬一页停顿时间
        self.WAIT_ONE_DATA = WAIT_ONE_DATA  # 每爬一条停顿时间
        self.ListNotifier = ListNotifier

    def main(self):
        """启动房天下爬虫"""
        self.reptile('sh')
        self.reptile('sz')
        self.reptile('bj')
        self.reptile('gz')

    def reptile(self, city_name_short):
        """生成详情页url列表,挨个访问详情页"""
        for urlDetail in self.generate_allurl(city_name_short):
            self.get_allurl(urlDetail, city_name_short)
            time.sleep(self.WAIT_ONE_PAGE)

    def generate_allurl(self, city_name_short):
        """生成url city_name_short=城市名称缩写"""
        if (city_name_short == 'bj'):
            url_p = 'http://zu.fang.com/house/h316-i3{}'
        else:
            url_p = 'http://zu.' + city_name_short + '.fang.com/house/h316-i3{}'
        for url_next in range(1, self.USER_IN_NUB)[::-1]:
            yield url_p.format(url_next)

    def get_allurl(self, url, city_name_short):
        """获取所有详情页的url"""
        try:
            r = requests.get(url, cookies=self.cookie, headers=self.headers)
            page = etree.HTML(r.text)
            # 获取详情页url列表
            housesUrlDiv = page.xpath(
                "//div[@class='houseList']/dl[@class='list hiddenMap rel']/dd[@class='info rel']/p[@class='title']/a")
            # 采集整租/合租(详情页很难采集到)
            types = page.xpath("//p[@class='font16 mt20 bold']/node()[1]")
            i = 0
            for index, a in enumerate(housesUrlDiv):
                i += 1
                if (city_name_short == 'bj'):
                    url_head = 'http://zu.fang.com'  # 详情页url开头
                else:
                    url_head = 'http://zu.' + city_name_short + '.fang.com'  # 详情页url开头
                self.open_url(url_head, index, a, types, city_name_short)
                time.sleep(self.WAIT_ONE_DATA)
        except Exception as err:
            print("访问列表页失败; url", url, "; errormsg:", err)

    def open_url(self, url, index, a, types, city_name_short):
        try:
            r = requests.get(url + a.get('href'), cookies=self.cookie, headers=self.headers)
            # print(r.content)
            # print(r.read())
            # break
            if r.status_code == 404:
                print(a.get('href') + 404)
                return
            page = etree.HTML(r.text)
            # 采集详情页
            try:
                # 去掉名字中的“-整租”，还要想办法解决名字前半部分有-的问题
                names = page.xpath("//div[@class='h1-tit rel']/h1")[0].text.split('-')
                name = ""
                if len(names) == 1:
                    name = names[0]
                for k in range(len(names) - 1):
                    name += names[k].replace(" ", "").replace("\n", "").replace("\r", "")
                name = name.replace('\r\n', '').replace(' ', '')  # 标题
                type = types[index].replace(" ", "").replace("\n", "").replace("\r", "")
                price = page.xpath("//strong[@class='red price bold']")[0].text.replace(" ", "").replace("\n",
                                                                                                         "").replace(
                    "\r", "")
                telephone = page.xpath("//span[@class='phoneicon floatl']")[0].text
                # addtime = page.xpath("//p[@class='gray9']/span[2]")[0].text.split('：')[-1]
                area = page.xpath("//ul[@class='house-info']/li[3]/a[2]")[0].text
                district = page.xpath("//ul[@class='house-info']/li[3]/a[1]")[0].text
                img_path_array = []
                picsinfo = page.xpath("//li[@class='slideshowItem']/a/img")
                for img in picsinfo:
                    img_path_array.append(img.get('src'))
                squarePattern = re.compile(r'^[0-9]+\.?[0-9]*')
                squareText = page.xpath("//ul[@class='house-info']/li[2]/span[@title='建筑面积']")[0].text.replace(" ",
                                                                                                               "").replace(
                    "\n", "").replace("\r", "")
                square = squarePattern.findall(squareText)[0]
                floor = page.xpath("//ul[@class='house-info']/li[2]/node()")[-5].replace(" ", "").replace("\r\n", "")
                if str(floor) == "":
                    floor = "暂无"
                direction = page.xpath("//ul[@class='house-info']/li[2]/node()")[-3].replace(" ", "").replace("\r\n",
                                                                                                              "")
            except Exception as err:
                # print(err)
                # print(url+a.get('href')+'爬取失败')
                return
            # 爬取房型信息（不一定有）
            try:
                shapeText = page.xpath("//ul[@class='house-info']/li[2]/node()")[3].replace(" ", "").replace("\r\n", "")
                shapePattern = re.compile(r'^\w+室\w*')
                if shapePattern.match("2室1厅"):
                    shape = shapeText
                else:
                    shape = "暂无"
            except Exception as err:
                # print(err)
                # shape = "暂无"
                # print(a.get('href') + '房型信息暂无')
                return

            # 采集地址信息(有的在span里，有的不在)
            try:
                address = page.xpath("//ul[@class='house-info']/li[@*]/node()[2]")[0].text
            except Exception as err:
                address = page.xpath("//ul[@class='house-info']/li[@*]/node()[2]")[0]

            # 爬取经纬度信息（单独爬取是因为有的房源没有这类信息）
            try:
                latlng = page.xpath("//div[@class='map-wrap mt20']/iframe")[0].get('src').split('?')[-1].split('&')
                for para in latlng:
                    para_now = para.split('=')
                    if para_now[0] == 'Baidu_coord_x':
                        lng = para_now[1]
                    elif para_now[0] == 'Baidu_coord_y':
                        lat = para_now[1]
            except Exception as err:
                lat = '暂无'
                lng = '暂无'
                #print(a.get('href') + '经纬度信息暂无')
                return

            # 打印进度
            # in_data = (
            # name, area, square, price, type, str(floor), str(shape), lat, lng, str(address), district, img_path_array,
            # str(telephone), str(direction), url + a.get('href'))
            info = {}
            info['cityName'] = city_name_short  # 城市名称缩写
            info['url'] = url + a.get('href')  # 详情页url
            info['title'] = name  # 标题
            info['locationPostition'] = [lng, lat]  # 经纬度
            info['rent'] = int(re.sub("\D", "", price))  # 租金
            info['rentStr'] = re.sub("\D", "", price)
            info['square'] = re.sub("\D", "", square)  # 面积 不带单位
            info['bedroomNum'] = re.findall(re.compile("(.*)室"), str(shape))[0]  # 卧室数量
            info['houseType'] = str(shape)  # 房屋类型
            info['floor'] = str(floor)  # 楼层
            info['orientation'] = str(direction)  # 朝向
            info['communityName'] = district  # 社区名称
            info['urbanDistrict'] = common.formatUrbanDistrict(city_name_short, area)  # 市区名称
            info['leasingMethod'] = type  # 租赁方式
            info['phone'] = str(telephone)  # 电话号
            info['imgPath'] = img_path_array  # 图片路径数组
            info['from'] = 'fangtx'  # 房天下
            info['createTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            print(info['createTime'],info['title'],info['url'])
            self.ListNotifier.appendNewData2List(info)
        except Exception as err:
            print("访问详情页:%s失败,错误信息:%s" % (url + a.get('href'), err))
