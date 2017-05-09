# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time
import csv
import os

class Crawler:
    def __init__(self, crawlArea = 'dongcheng'):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3)'
        self.headers = { 'User-Agent' : self.user_agent }
        self.links = []
        self.crawlArea = crawlArea

    def getPageLimit(self):
        try:
            url = 'http://bj.lianjia.com/ershoufang/' + self.crawlArea
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            # print pageCode
            # Get limit from pageCode
            pattern = re.compile('totalPage":(.*?),')
            item = re.findall(pattern, pageCode)
            return int(item[0])

        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print "Get page limit failed...",e.reason
                return 0

    def getPageCode(self, url):
        try:
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            print "Geting page code of " + url + " ..."
            return pageCode
 
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print "Connection failed...",e.reason
                quit()
                return None
 	
 	# Extract links in one page and add it to memory
 	# If no more link, return false
    def addLinks(self, pageCode):
 		pattern = re.compile('<li class="clear"><a class="img " href="(.*?)" target')
		items = re.findall(pattern, pageCode)
		if(len(items) <= 0):
			print("No links!")
			quit()
		self.links.extend(items)

    def crawlPage(self, pageCode):
        print "Crawl page..."

        def getReItem(pattern, pageCode):
            re_pattern = re.compile(pattern)
            items = re.findall(re_pattern, pageCode)
            if len(items) <= 0:
                print "CANNOT crawl this page."
                quit()
            return items[0]

        with open('test.htm', 'r') as myfile:
                pageCode = myfile.read()
        print "Crawl page..."

        ret = []
        # 标题
        pattern = '<h1 class="main" title="(.*?)">'
        item = getReItem(pattern)
        title = str(item)
        ret.append(title)

        # 价格，均价，小区名称，所在区域
        pattern = '<div class="overview">.*?<div class=".*?price.*?"><span class="total">(.*?)</span>' + \
            '<span class="unit"><span>(.*?)</span>.*?' + \
            '<span class="unitPriceValue">(.*?)<i>(.*?)</i>.*?' + \
            '小区名称.*?</span>.*?<a.*?>(.*?)</a>.*?' + \
            '所在区域.*?</span>.*?<a.*?>(.*?)</a>.*?'
        item = getReItem(pattern, pageCode)
        price = str(item[0]) + str(item[1])
        avgPrice = str(item[2]) + str(item[3])
        court = str(item[4])
        area = str(item[5])
        ret.append(price)
        ret.append(avgPrice)
        ret.append(court)
        ret.append(area)

        ## 基本属性
        # 房屋户型
        pattern = '<li><span class="label">房屋户型</span>(.*?)</li>'
        item = getReItem(pattern, pageCode)
        ret.append(str(item))
        # 所在楼层
        pattern = '<li><span class="label">所在楼层</span>(.*?)</li>'
        item = getReItem(pattern, pageCode)
        ret.append(str(item))
        # 建筑面积
        pattern = '<li><span class="label">建筑面积</span>(.*?)</li>'
        item = getReItem(pattern, pageCode)
        ret.append(str(item))
        # 户型结构
        pattern = '<li><span class="label">户型结构</span>(.*?)</li>'
        item = getReItem(pattern, pageCode)
        ret.append(str(item))
        # 套内面积
        pattern = '<li><span class="label">套内面积</span>(.*?)</li>'
        item = getReItem(pattern, pageCode)
        ret.append(str(item))
        # 建筑类型
        pattern = '<li><span class="label">建筑类型</span>(.*?)</li>'
        item = getReItem(pattern, pageCode)
        ret.append(str(item))
        # 房屋朝向
        pattern = '<li><span class="label">房屋朝向</span>(.*?)</li>'
        item = getReItem(pattern, pageCode)
        ret.append(str(item))
        # 建筑结构
        pattern = '<li><span class="label">建筑结构</span>(.*?)</li>'
        item = getReItem(pattern, pageCode)
        ret.append(str(item))
        # 装修情况
        pattern = '<li><span class="label">装修情况</span>(.*?)</li>'
        item = getReItem(pattern, pageCode)
        ret.append(str(item))
        # 梯户比例
        pattern = '<li><span class="label">梯户比例</span>(.*?)</li>'
        item = getReItem(pattern, pageCode)
        ret.append(str(item))
        # 供暖方式
        pattern = '<li><span class="label">供暖方式</span>(.*?)</li>'
        item = getReItem(pattern, pageCode)
        ret.append(str(item))
        # 配备电梯
        pattern = '<li><span class="label">配备电梯</span>(.*?)</li>'
        item = getReItem(pattern, pageCode)
        ret.append(str(item))
        # 产权年限
        pattern = '<li><span class="label">产权年限</span>(.*?)</li>'
        item = getReItem(pattern, pageCode)
        ret.append(str(item))

        return ret

    def start(self):
        print "Start Crawling..."
#        proxy = urllib2.ProxyHandler({'http': '127.0.0.1:9050'})
#        opener = urllib2.build_opener(proxy)
#        urllib2.install_opener(opener)
#        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
#        socket.socket = socks.socksocket
#        t = threading.Timer(60, self.reloadTor)
#        t.start()

        # pageLimit = self.getPageLimit()
        # print('Page limit is ' + str(pageLimit))
        # # Load all pages
        # while(self.pageIndex <= pageLimit):
        # 	print "Loading page " + str(self.pageIndex) + "..."
        # 	url = 'http://bj.lianjia.com/ershoufang/' + self.crawlArea + '/pg' + str(self.pageIndex)
        # 	pageCode = self.getPageCode(url)
        # 	self.addLinks(pageCode)
        # 	self.pageIndex = self.pageIndex + 1
        # list_file = open(os.getcwd() + '/' + str(self.crawlArea) +'_list.csv', 'w')
        # for item in self.links:
        #     list_file.write("%s\n" % item)

        # Crawling pages
        with open(os.getcwd() + '/' + str(self.crawlArea) +'.csv', 'a') as f:
            writer = csv.writer(f)
            index = ['标题','价格','均价','小区名称','所在区域','房屋户型','所在楼层','建筑面积', '户型结构',\
            '套内面积','建筑类型','房屋朝向','建筑结构','装修情况','梯户比例','供暖方式','配备电梯','产权年限']
            writer.writerow(index)

            links_list = []
            with open(os.getcwd() + '/' + str(self.crawlArea) +'_list.csv', 'rb') as f:
                reader = csv.reader(f)
                links_list = list(reader)

            for link in links_list:
                pageCode = self.getPageCode(link)
                row = self.crawlPage(pageCode)
                writer.writerow(row)

