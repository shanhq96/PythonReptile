import urllib.request
import http.cookiejar
import time
from lxml import etree
import re
import common


class AnjukeReptile():
    """安居客爬虫类"""

    def make_my_opener(self, head={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'sessid=0042B3A7-A9AD-40F7-DD3F-03C4F4561877; als=0; tuangou_list_ids=2%3A4; isp=true; Hm_lvt_c5899c8768ebee272710c9c5f365a6d8=1497426142; Hm_lpvt_c5899c8768ebee272710c9c5f365a6d8=1497426142; isp=true; lps=http%3A%2F%2Fsh.zu.anjuke.com%2Ffangyuan%2Fp1-px3%2F%7C; _ga=GA1.2.1494529036.1497419119; _gid=GA1.2.180205610.1497579590; propertys=hr0m1b-orn06l_; ctid=14; __xsptplusUT_8=1; ajk_member_captcha=58d6136e5f38f5b240deb52e7117929a; ajk_member_name=%E6%89%8B%E6%9C%BA6411497626365; ajk_member_key=5405399a6b9ed46b1bf77a3cc71e65d6; ajk_member_time=1529162340; aQQ_ajkauthinfos=5MsU2zVQf25h2T0VdZmu9vwo3HB%2FQZeQPVnvxuy4kS3WImPEqWpPTEGh8Zdq%2ButcMvtovbneAuhG%2FatLYiM8XnhBFu0rgetk6sAY; lui=40331122%3A1; __xsptplus8=8.7.1497626220.1497626367.3%234%7C%7C%7C%7C%7C%23%23Ge2gaxxz8SVMNKNH8KVcBoX5A7jbSf-D%23; aQQ_ajkguid=3FCF181F-0531-B86C-DDEB-5E07EA984B05; 58tj_uuid=585662d8-619b-4bab-8c3b-ac53b2f37d8f; new_session=0; init_refer=; new_uv=8; ajk_member_id=40331122; twe=2',
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
        """启动安居客爬虫"""
        self.reptile('gz')
        self.reptile('bj')
        self.reptile('sh')
        self.reptile('sz')


    def reptile(self, city_name_short):
        """生成详情页url列表,挨个访问详情页"""
        for urlDetail in self.generate_allurl(city_name_short):
            self.get_allurl(urlDetail, city_name_short)
            time.sleep(self.WAIT_ONE_PAGE)

    def generate_allurl(self, city_name_short):
        """生成列表页url city_name_short=城市名称缩写"""
        url_p = 'https://' + city_name_short + '.zu.anjuke.com/fangyuan/p{}-px3/'
        for url_next in range(1, self.USER_IN_NUB)[::-1]:
            yield url_p.format(url_next)

    def get_allurl(self, url, city_name_short):
        """获取所有详情页的url"""
        try:
            uop = self.OPER.open(url, timeout=1000)
            data = uop.read().decode('utf-8')
            page = etree.HTML(data)
            # r = requests.get(url, cookies=self.cookie, headers=self.headers, allow_redirects=False)
            # page = etree.HTML(r.text)
            # 获取url列表
            housesUrlDiv = page.xpath("//div[@class='zu-info']/h3/a[1]")
            i = 0
            for a in housesUrlDiv:
                i += 1
                self.open_url(url, a, city_name_short)
                time.sleep(self.WAIT_ONE_DATA)
        except Exception as err:
            print("访问列表页失败; url", url, "; errormsg:", err)

    def open_url(self, url, a, city_name_short):
        try:
            # r = requests.get(a.get('href'), cookies=self.cookie, headers=self.headers, allow_redirects=False)
            uop = self.OPER.open(a.get('href'), timeout=1000)
            if uop.code != 200:
                print("目标链接:(%s)数据无效,状态码:%s" % (a.get('href'), uop.code))
                return
            data = uop.read().decode('utf-8')  # python3
            # if r.status_code != 200:
            #     print("目标链接:(%s)数据无效,状态码:%s"%(a.get('href'),r.status_code))
            #     return
            # page = etree.HTML(r.text)
            page = etree.HTML(data)

            # 爬取详情页
            try:
                name = page.xpath("//h3[@class='fl']")[0].text
                square = page.xpath(
                    "//div[@class='pinfo']/div[@class='box']/div[@class='phraseobox cf']/div[@class='ritem fr']/dl[@class='p_phrase cf'][2]/dd")[
                    0].text
                price = page.xpath(
                    "//div[@class='pinfo']/div[@class='box']/div[@class='phraseobox cf']/div[@class='litem fl']/dl[@class='p_phrase cf'][1]/dd/strong/span")[
                    0].text
                type = page.xpath(
                    "//div[@class='pinfo']/div[@class='box']/div[@class='phraseobox cf']/div[@class='litem fl']/dl[@class='p_phrase cf'][4]/dd")[
                    0].text
                floor = page.xpath(
                    "//div[@class='pinfo']/div[@class='box']/div[@class='phraseobox cf']/div[@class='ritem fr']/dl[@class='p_phrase cf'][4]/dd")[
                    0].text
                shape = page.xpath(
                    "//div[@class='pinfo']/div[@class='box']/div[@class='phraseobox cf']/div[@class='litem fl']/dl[@class='p_phrase cf'][3]/dd")[
                    0].text
                pics = ''
                picsinfo = page.xpath(
                    "//div[@class='tabscon tnow']/div[@class='bigps photoslide cf']/div[@class='picCon']/ul[@class='picMove cf']/li/a/img")
                img_path_array = []
                for img in picsinfo:
                    img_path_array.append(img.get('src'))
                telephone = page.xpath("//p[@class='broker-mobile']/node()")[1]
                direction = page.xpath(
                    "//div[@class='pinfo']/div[@class='box']/div[@class='phraseobox cf']/div[@class='ritem fr']/dl[@class='p_phrase cf'][3]/dd")[
                    0].text
                addtime = \
                page.xpath("//div[@class='pro_detail']/div[@class='text-mute extra-info']")[0].text.split('，')[
                    -1].split('：')[-1]
            except:
                # print(a.get('href')+'爬取失败')
                return
                # input()

            # 爬取行政区信息（单独爬取是因为有的房源没有行政区信息）
            try:
                area = page.xpath(
                    "//div[@class='pinfo']/div[@class='box']/div[@class='phraseobox cf']/div[@class='litem fl']/dl[@class='p_phrase cf'][6]/dd/a[1]")[
                    0].text
            except:
                area = '暂无'
                # print(a.get('href') + '区域信息暂无')
                return
                # input()

            # 爬取经纬度及地址信息（单独爬取是因为有的房源没有这类信息）
            try:
                latlng = page.xpath(
                    "//div[@class='cinfo']/div[@class='box']/div[@class='phraseobox cf']/div[@class='litem fl']/dl[@class='p_phrase cf'][3]/dd/a")[
                    0].get('href')
                lng = latlng.split('?')[-1].split('&')[0].split('=')[1]
                lat = latlng.split('?')[-1].split('&')[1].split('=')[1]
                address = page.xpath(
                    "//div[@class='cinfo']/div[@class='box']/div[@class='phraseobox cf']/div[@class='litem fl']/dl[@class='p_phrase cf'][3]/dd")[
                    0].text
                district = page.xpath(
                    "//div[@class='cinfo']/div[@class='box']/div[@class='phraseobox cf']/div[@class='litem fl']/dl[@class='p_phrase cf'][1]/dd/a")[
                    0].text
            except:
                lat = '暂无'
                lng = '暂无'
                address = '暂无'
                district = '暂无'
                # print(a.get('href') + '小区信息暂无')
                return
                # input()

            # in_data = (
            # name, area, square, price, type, floor, shape, lat, lng, address, district, pics, str(telephone), direction,
            # addtime, a.get('href'))

            info = {}
            info['cityName'] = city_name_short  # 城市名称缩写
            info['url'] = a.get('href')  # 详情页url
            info['title'] = name  # 标题
            info['locationPostition'] = [lat, lng]  # 经纬度
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
            info['from'] = 'anjuke'  # 房天下
            info['createTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            print(info['createTime'],info['title'],info['url'])
            self.ListNotifier.appendNewData2List(info)
        except Exception as err:
            print("访问详情页:%s失败,错误信息:%s" % (url, err))
