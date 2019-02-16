from threading import Thread
import sqlite3
import re
import requests
from wx.lib.pubsub import pub


class EmailThread(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data = data
        self.db = sqlite3.connect("data/data.db", check_same_thread=False)
        self.cursor = self.db.cursor()
        self.stopMessage = 0

    def run(self):
        sql = 'UPDATE search SET ok=1 WHERE id=%s'
        sql2 = 'INSERT INTO contact(name,host,email,url) VALUES ("%s","%s","%s","%s")'
        for x in self.data:
            if self.stopMessage:
                break
            cid = x[0]
            query_name = x[1]
            url = x[2]
            try:
                Emails, host = self.findUrl(url)
                # print('找到联系邮箱：')
                for email in Emails:
                    # print(email)
                    if email[-4:] == '.com':
                        self.cursor.execute(
                            sql2 %
                            (query_name, host, email, url))
                        self.db.commit()
                self.cursor.execute(sql, (cid))
                self.db.commit()
            except BaseException:
                pass

    def stop(self):
        self.stopMessage = 1

    def findContact(self, host, text):
        p = r'<a href="(.*?)"'
        contact_url = ''
        contactUrls = re.findall(p, text)
        for x in contactUrls:
            x = x.lower()
            if x.find('contact') >= 0:
                contact_url = x
                break
        if len(contact_url) < 1:
            return ""
        if contact_url[0] == '/':
            contact_url = host + contact_url
        elif contact_url[0:4] == 'http':
            pass
        else:
            contact_url = host + '/' + contact_url
        return contact_url

    def findMsg(self, text):
        text = text.replace('(at)', '@')
        dict_email = re.findall(
            r'[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*@[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*', text)
        return list(dict_email)

    def getHttpText(self, url):
        headers = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
        }
        try:
            html = requests.get(url, headers=headers, timeout=10).text
        except BaseException:
            html = ''
        return html

    def findUrl(self, url):
        # print('正在爬取的页面：', url)
        p = r'(http[s]*:\/\/[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+)\/'
        host = re.findall(p, url)[0][0]
        hostText = self.getHttpText(url)
        contact_url = self.findContact(host, hostText)
        if len(contact_url) > 0:
            # print('联系页面：', contact_url)
            contactText = self.getHttpText(contact_url)
            Emails = self.findMsg(contactText)
            return Emails, host
        else:
            # print('没有找到联系页面：')
            Emails = self.findMsg(hostText)
            Emails = list(set(Emails))
            return Emails, host
