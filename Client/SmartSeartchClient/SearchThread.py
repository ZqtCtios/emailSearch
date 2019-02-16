from threading import Thread
from wx.lib.pubsub import pub
import wx
import sqlite3
from selenium import webdriver
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import EmailThread
import OutPutFile


class TestThread(Thread):
    def __init__(self, test):
        # 线程实例化时立即启动
        Thread.__init__(self)
        self.running = 1
        self.db = sqlite3.connect("data/data.db", check_same_thread=False)
        self.cursor = self.db.cursor()
        self.test = test

    def okUrl(self, url, options):
        try:
            for x in options:
                if url.find(x) > 0:
                    return False
        except BaseException:
            return False
        return True

    def searchBing(self, query_name, options, browser):
        query = query_name
        url = 'https://cn.bing.com/search?q={}&ensearch=1'.format(query_name)
        page = 0
        while True:
            if self.running == 0:
                break
            if self.test and page >= 5:
                break
            page += 1
            self.MessagePrint("正在爬取第{}页".format(page))
            browser.get(url)
            oldUrl = url
            soup = BeautifulSoup(browser.page_source, "lxml")
            lis = soup.find_all('li', attrs={'class': 'b_algo'})
            for li in lis:
                h2 = li.h2
                a = h2.a
                title = a.text
                url = a["href"]
                if self.okUrl(url, options):
                    try:
                        self.cursor.execute(
                            'insert into search(name,page,title,url,ok) values("%s",%s,"%s","%s",%s)' %
                            (query_name, page, title, url, 0))
                    except BaseException:
                        pass
            self.db.commit()

            try:
                url = browser.find_element_by_xpath(
                    '//a[@title="Next page"]').get_attribute('href')
            except BaseException:
                return page
            print(url,oldUrl)
            if url == oldUrl:
                break
        return page

    def filter_link(self, link):
        try:
            o = urlparse(link, 'http')
            if o.netloc:
                return link
            if link.startswith('/url?'):
                link = parse_qs(o.query)['q'][0]
                o = urlparse(link, 'http')
                if o.netloc:
                    return link
        except Exception as e:
            return None

    def searchGoogle(self, query_name, options, browser):
        query = query_name
        page = 0
        while True:
            if self.running == 0:
                break
            if self.test and page >= 5:
                break
            self.MessagePrint("正在爬取第{}页".format(page + 1))
            sum = page * 10
            yes = True
            if page == 0:
                url = 'https://www.google.com/search?q={}&filter=0'.format(
                    query.replace(' ', '+'))
                browser.get(url)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            for x in soup.find_all('div', class_='r'):
                yes = False
                a = x.a
                title = a.text
                url = a['href']
                url = self.filter_link(url)
                if self.okUrl(url, options):
                    try:
                        self.cursor.execute(
                            'insert into search(name,page,title,url,ok) values("%s",%s,"%s","%s",%s)' %
                            (query_name, page, title, url, 0))
                    except BaseException:
                        pass
            self.db.commit()
            #time.sleep(random.randint(0.5, 1))
            page += 1
            if yes:
                self.MessagePrint("爬取谷歌失败，启用Bing重新搜索")
                return -1
            try:
                next = browser.find_element_by_xpath(
                    '//*[@id="pnnext"]/span[2]')
                next.click()
            except BaseException:
                break
        return page

    def testGoogle(self):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        browser = webdriver.Chrome(chrome_options=option)
        browser.get('https://www.google.com')
        html = browser.page_source
        browser.close()
        if len(html) < 100:
            return False
        return True

    def run(self):
        #try:
        wx.CallAfter(pub.sendMessage, "lock", msg=1)
        self.running == 1
        self.cursor.execute("delete from search")
        self.cursor.execute(
            "update sqlite_sequence set seq = 0 where name =\"search\"")
        self.cursor.execute("delete from contact")
        self.cursor.execute(
            "update sqlite_sequence set seq = 0 where name =\"contact\"")
        queryList, options = self.readListData()
        self.MessagePrint("读取数据库")
        self.MessagePrint("正在测试谷歌连通性。。。。。")
        yes = self.testGoogle()
        if yes:
            self.MessagePrint("成功，启用Google搜索")
        else:
            self.MessagePrint("失败，启用Bing搜索")
        for queryName in queryList:
            if self.running == 0:
                break
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            browser = webdriver.Chrome(chrome_options=option)
            self.MessagePrint("开始搜索字段：{}.......".format(queryName))
            if not yes:
                page = self.searchBing(queryName, options, browser)
            else:
                page = self.searchGoogle(queryName, options, browser)
            if page == -1 or yes:
                self.MessagePrint("启用Bing搜索")
                page = self.searchBing(queryName, options, browser)
            self.MessagePrint('共搜寻{}页'.format(page))
            browser.close()
            if self.running == 0:
                break

            self.findEmail(queryName)
            if self.running == 0:
                break
            self.MessagePrint("Email搜寻完毕\n 输出xls文件")
            fileMaker = OutPutFile.DataToFile(queryName)
            fileMaker.work()
            self.MessagePrint("成功\n")
            if self.test:
                self.cursor.execute("update test set test=1")
                self.db.commit()
                break
        # except BaseException:
        #     self.MessagePrint("浏览器出错")
        wx.CallAfter(pub.sendMessage, "update", msg=0)
        wx.CallAfter(pub.sendMessage, "lock", msg=0)
        self.db.close()

    def getdata(self, queryName):
        sql = 'SELECT id,name,url FROM search where ok=0 and  name="%s" group by url' % (
            queryName)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def findEmail(self, queryName):
        data = self.getdata(queryName)
        dataLen = len(data)
        self.MessagePrint("共搜索{}个结果".format(dataLen))
        self.MessagePrint("后台开始搜寻Email，数据量较大，根据网速快慢，大约在10-40分钟不等，请耐心等待。。。。")
        tnum = 10
        x = dataLen // tnum
        self.Thead = []
        for r in range(0, tnum):
            t = EmailThread.EmailThread(data[r * x:r * x + x])
            self.Thead.append(t)
        t = EmailThread.EmailThread(data[x * tnum:dataLen])
        self.Thead.append(t)
        for t in self.Thead:
            t.start()
        for t in self.Thead:
            t.join()

    def readListData(self):
        self.cursor.execute("select * from searchLine where hasDone=0")
        data = self.cursor.fetchall()
        searchList = []
        for lint in data:
            searchList.append(lint[1])
        options = []
        self.cursor.execute("select * from blockLine")
        data = self.cursor.fetchall()
        for lint in data:
            options.append(lint[1])
        return searchList, options

    def MessagePrint(self, string):
        string = string + "\n"
        wx.CallAfter(pub.sendMessage, "update", msg=string)

    def stop(self):
        self.running = 0
        try:
            for t in self.Thead:
                t.stop()
        except BaseException:
            pass
