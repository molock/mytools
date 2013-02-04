# -*- coding: utf-8 -*-
import sqlite3
import os,platform,re

importDir = r'D:\游戏市场分析\市场分析'

class Data_reader():
    file_dict = {}
    reg_rule =('','')
    EXCEL_match_reg = r'\.xls(x)?(m)?'
    EXCEL_sub_reg = r"(\.xlsx)?(\.xlsm)?"

    def __init__(self,match_reg= False,sub_reg = False):
        if match_reg:
            self.EXCEL_match_reg = match_reg
        if sub_reg:
            self.EXCEL_match_reg = sub_reg

    def get_file_dict(self,rootdir):
        #参数是utf-8编码的，需要变成操作系统相应的编码格式
        if platform.system() == 'Windows':
            rootdir = rootdir.decode(encoding='utf-8').encode(encoding='GB2312')

        for root,dirs,files in os.walk(rootdir):
            for file in files:
                file_path = os.path.join(root,file)
                #把从操作系统读取到的字符串转为utf-8编码
                if platform.system() == 'Windows':
                    file_path = file_path.decode(encoding='GB2312').encode(encoding='utf-8')
                    file = file.decode(encoding='GB2312').encode(encoding='utf-8')
                    #只读取以.xlsx或.xlsm为后缀的文件
                    if re.match(self.EXCEL_match_reg,file):
                        file = re.sub(self.EXCEL_sub_reg,'',file)
                        print file,':',file_path
                        self.file_dict[file] = file_path
        print self.file_dict
        return self.file_dict

    def get_excel_data(self,file_path):
        #获取文件字典中的所有excel文件
        if not re.match(self.EXCEL_match_reg,file_path):
            print file_path,'is not excel file!'
            pass




if __name__ == "__main__":
    reader = Data_reader()
    reader.get_file_dict(importDir)

class Data_writer():
    file_dict = {}
    dbName = ''

    #构造方法，需要传入数据库名称
    def __init__(self,db,fileDict):
        self.db = db
        self.fileDict = fileDict

    #连接数据库
    def re_connDB(self,db):
        self.db = db
        conn = sqlite3.connect(self.db)
        curs = conn.cursor()
        return curs

    #创建一个数据表
    def create_table(self,table,title_list,data_list=False):
        arr_title =''
        arr_n = ''
        for index,arr in enumerate(title_list):
            title_list[index] = arr + ' ' + 'TEXT'
            print index
            if index == 0:
                arr_title = title_list[index]
                arr_n = '?'
            else:
                arr_title = arr_title + ','+title_list[index]
                arr_n = arr_n + ',' + '?'
            print title_list
            print arr_n

        conn = sqlite3.connect(self.db)
        curs = conn.cursor()
        curs.execute("CREATE TABLE %s(%s)" % (table,arr_title))
        print "CREATE TABLE %s(%s)" % (table,arr_title)

        if data_list:
            query = 'INSERT INTO %s VALUES (%s)' %(table,arr_n)
            for line in data_list:
                curs.execute(query,line)

        conn.commit()
        conn.close()


    def insert_data(self,dataList):
        pass
