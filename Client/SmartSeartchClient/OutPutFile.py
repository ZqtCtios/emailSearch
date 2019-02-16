import xlwt
import sqlite3
import os


class DataToFile():
    def __init__(self, qureyName):
        self.qureyName = qureyName
        self.db = sqlite3.connect("data/data.db", check_same_thread=False)
        self.cursor = self.db.cursor()
        path = os.getcwd() + '/OutPut/' + qureyName
        try:
            os.mkdir(path)
        except BaseException:
            pass

    def getData(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def ContactToFile(self):
        sql = 'select host,email,url from contact where name =\"{}\" group by email order by host'.format(
            self.qureyName)
        data = self.getData(sql)
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('data')
        worksheet.write(0, 0, "ID")
        worksheet.write(0, 1, "HostName")
        worksheet.write(0, 2, "Email")
        worksheet.write(0, 3, "SourcePage")
        for i in range(len(data)):
            worksheet.write(i + 1, 0, i + 1)
            worksheet.write(i + 1, 1, data[i][0])
            worksheet.write(i + 1, 2, data[i][1])
            worksheet.write(i + 1, 3, data[i][2])
        workbook.save("./OutPut/{}/ContactEmail.xls".format(self.qureyName))

    def SearchToFile(self):
        sql = 'select * from search  where name =\"{}\"'.format(self.qureyName)
        data = self.getData(sql)
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('data')
        worksheet.write(0, 0, "ID")
        worksheet.write(0, 1, "Page")
        worksheet.write(0, 2, "Title")
        worksheet.write(0, 3, "Url")
        for i in range(len(data)):
            worksheet.write(i + 1, 0, i + 1)
            worksheet.write(i + 1, 1, data[i][2])
            worksheet.write(i + 1, 2, data[i][3])
            worksheet.write(i + 1, 3, data[i][4])
        workbook.save("./OutPut/{}/SearchResult.xls".format(self.qureyName))

    def work(self):
        self.SearchToFile()
        self.ContactToFile()
