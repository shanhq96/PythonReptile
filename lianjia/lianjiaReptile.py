# -*- coding: utf-8 -*
# !/usr/bin/env python
import re
from bs4 import BeautifulSoup
import urllib.request
import http.cookiejar
import time
import common


class LianjiaReptile():
    """链家爬虫类"""

    def make_my_opener(self, head={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'zufang_huodong_show=1; lianjia_uuid=9dd0d410-d30b-45a8-82a0-9b835cccd22f; all-lj=c28812af28ef34a41ba2474a2b5c52c2; UM_distinctid=15ca58e09d67a-099529ab5cdc34-701238-151800-15ca58e09d7143; sample_traffic_test=controlled_68; _jzqckmp=1; gr_user_id=9b572d4b-6829-4d88-8dc6-66937ad37d96; cityCode=sh; ubt_load_interval_b=1497593531715; ubtd=25; __xsptplus696=696.1.1497588980.1497593532.19%234%7C%7C%7C%7C%7C%23%23OXJB4Mjvle-tKYF2AuqGxApZyzMhJO2g%23; ubta=2299869246.1290169133.1497588975938.1497593534036.1497593535305.25; ubtc=2299869246.1290169133.1497593535306.7D8E7E31781482C3AFC56016A8A78598; select_city=110000; _jzqx=1.1497589018.1497595835.2.jzqsr=sh%2Elianjia%2Ecom|jzqct=/.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/; lianjia_token=2.006f9300bb16f65d947e3e298aa7232bec; _smt_uid=5940e8f8.39cba54e; CNZZDATA1253477573=1127617539-1497424592-%7C1497600155; CNZZDATA1254525948=339452706-1497423464-%7C1497597949; CNZZDATA1255633284=1079592254-1497576440-%7C1497598061; CNZZDATA1255604082=214885118-1497425476-%7C1497601155; _jzqa=1.3277915027281347600.1497426169.1497595835.1497601441.6; _jzqc=1; _jzqb=1.5.10.1497601441.1; _qzja=1.661993136.1497426169827.1497595834943.1497601440998.1497601500734.1497601641473.0.0.0.25.6; _qzjb=1.1497601440998.5.0.0.0; _qzjc=1; _qzjto=23.5.0; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _ga=GA1.2.1231883914.1497426171; _gid=GA1.2.1819351555.1497578170; _gat_dianpu_agent=1; lianjia_ssid=c89b7ec2-8641-4c05-b12a-2852bf9cf964',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'
    }):
        """head:dict of header"""
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        header = []
        for key, value in head.items():
            elem = (key, value)
            header.append(elem)
        opener.addheaders = header
        return opener

    def __init__(self, ListNotifier,USER_IN_NUB,WAIT_ONE_PAGE,WAIT_ONE_DATA):
        """初始化opener,每次爬的页数,通知者"""
        self.OPER = self.make_my_opener()
        self.USER_IN_NUB = USER_IN_NUB  # 爬的页数
        self.WAIT_ONE_PAGE = WAIT_ONE_PAGE  # 每爬一页停顿时间
        self.WAIT_ONE_DATA = WAIT_ONE_DATA  # 每爬一条停顿时间
        self.ListNotifier = ListNotifier

    def main(self):
        """启动链家爬虫"""
        self.reptile('bj')
        self.reptile('sz')
        self.reptile('gz')

    def reptile(self, city_name_short):
        """爬虫主体程序"""
        for i in self.generate_allurl(city_name_short):
            self.get_allurl(i, city_name_short)
            time.sleep(self.WAIT_ONE_PAGE)

    def generate_allurl(self, city_name_short):
        """生成url city_name_short=城市名称缩写"""
        url = 'https://' + city_name_short + '.lianjia.com/zufang/rco10/pg{}/'
        for url_next in range(1, self.USER_IN_NUB)[::-1]:
            yield url.format(url_next)

    def get_allurl(self, url, city_name_short):
        """获取所有详情页的url"""
        try:
            uop = self.OPER.open(url, timeout=1000)
            data = uop.read().decode()
            re_set = re.compile(
                '<li.*? data-index="\d*" data-id="\w*">.*?<div class="info-panel"><h2>.*?<a.*? target="_blank" href="(.*?)"')
            re_get = re.findall(re_set, data)
            for re_get_url in re_get:
                self.open_url(re_get_url, city_name_short)
                time.sleep(self.WAIT_ONE_DATA)
        except Exception as err:
            print("访问列表页失败; url", url, "; errormsg:", err)

    def open_url(self, re_get_url, city_name_short):
        """爬取详情页数据"""
        try:
            uop = self.OPER.open(re_get_url, timeout=1000)
            data = uop.read()
            data = data.decode('utf-8')  # python3
            info = {}
            soup = BeautifulSoup(data, 'lxml')
            info['cityName'] = city_name_short  # 城市名称缩写  北京:bj  深圳:sz 上海:sh 广洲:gz
            info['url'] = re_get_url  # 链接
            info['title'] = soup.select('.main')[0].text  # 标题
            locationPattern = re.compile(
                '<script>[\s\S]*require\(\[\'detail/zufang\'\],function\(init\)[\s\S]*resblockPosition:\'(.*)\'[\s\S]*</script>')
            locationTemp = re.findall(locationPattern, data)[0]  # 经纬度
            info['locationPostition'] = [locationTemp.split(',')[0],locationTemp.split(',')[1]] # 经纬度
            info['rent'] = int(re.sub("\D", "", soup.select('.total')[0].text))  # 租金 不带单位
            info['rentStr'] = re.sub("\D", "", soup.select('.total')[0].text)   # 租金字符串
            squarePattern = re.compile('^(\d*).*$')
            info['square'] = re.findall(squarePattern, soup.select('.lf')[0].next.nextSibling)[0]  # 面积 不带单位
            #info['square'] = re.sub("\D", "", soup.select('.lf')[0].next.nextSibling)  # 面积 不带单位
            info['bedroomNum'] = re.findall(re.compile("(.*)室"), soup.select('.lf')[1].next.nextSibling.split(' ')[0])[0]    # 卧室数量
            info['houseType'] = soup.select('.lf')[1].next.nextSibling.split(' ')[0]  # 房屋户型
            info['floor'] = soup.select('.lf')[2].next.nextSibling  # 楼层
            info['orientation'] = soup.select('.lf')[3].next.nextSibling  # 房屋朝向
            info['communityName'] = soup.select('.zf-room p')[5].next.nextSibling.text  # 社区名称
            urbanDistrictTemp = soup.select('.zf-room p')[6].next.nextSibling.text
            info['urbanDistrict'] = common.formatUrbanDistrict(city_name_short,urbanDistrictTemp)  # 市区名称
            info['leasingMethod'] = soup.select('.introduction .introContent .base .content ul li')[
                0].next.nextSibling  # 租赁方式
            info['phone'] = soup.select('.brokerInfo .brokerInfoText .phone')[0].text.replace('\n', '').replace(' ',
                                                                                                                '')  # 联系方式
            img_path_nodes = soup.select('.overview .img .thumbnail ul li')
            img_path_array = []
            for img_path_node in img_path_nodes:
                img_path_array.append(img_path_node['data-src'])
            info['imgPath'] = img_path_array  # 图片路径数组
            info['from'] = 'lianjia'  # 来源信息 lianjia
            info['createTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

            print(info['createTime'],info['title'],info['url'])
            self.ListNotifier.appendNewData2List(info)
        except Exception as err:
            print("访问详情页失败; url", re_get_url, "; errormsg:", err)
