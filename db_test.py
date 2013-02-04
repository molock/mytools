#coding=utf-8
import sqlite3,sys
db = 'testdb'
table = 'buff表1'
title = ['ID','等级']
list = [['600000001','1'],['750000017','1']]

#创建表，并输入数据
def create_table_data(db,table,title,list):
    dbname = db
    table_name = table
    title_list = title
    data_list = list
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

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute("CREATE TABLE %s(%s)" % (table_name,arr_title))
    print "CREATE TABLE %s(%s)" % (table_name,arr_title)

    query = 'INSERT INTO %s VALUES (%s)' %(table_name,arr_n)
    for line in data_list:
        curs.execute(query,line)

    conn.commit()
    conn.close()

#只创建表内的表头，不输入数据
def create_table(db,table,title):
    table_name = table
    title_list = title
    arr_title =''

    for index,arr in enumerate(title_list):
        title_list[index] = arr + ' ' + 'TEXT'
        print index
        if index == 0:
            arr_title = title_list[index]
        else:
            arr_title = arr_title + ','+title_list[index]
        print title_list

    conn = sqlite3.connect(db)
    curs = conn.cursor()
    curs.execute("CREATE TABLE %s(%s)" % (table_name,arr_title))
    print "CREATE TABLE %s(%s)" % (table_name,arr_title)

    conn.commit()
    conn.close()

#在指定的表内追加数据
def insert_table(db,table,data):
    conn = sqlite3.connect(db)
    curs = conn.cursor()
    for index,arr in enumerate(data):
        if index == 0:
            arr_n = '?'
        else:
            arr_n = arr_n + ',' + '?'

    query = 'INSERT INTO %s VALUES (%s)' %(table,arr_n)
    for line in data:
        curs.execute(query,line)

def get_data(db,table):
    conn = sqlite3.connect(db)
    curs = conn.cursor()
    query = 'SELECT * FROM %s' %table
    print query
    curs.execute(query)
    for row in curs:
        print row
    conn.close()

def del_table(db,table):
    conn = sqlite3.connect(db)
    curs = conn.cursor()
    query = 'DROP TABLE %s' %table
    curs.execute(query)
    print curs.fetchall()
    conn.close()


if __name__ == "__main__":
    #create_table_data(db,table,title,list)
    #create_table(db,table,title)
    #insert_table(db,table,list)
    get_data(db,table)
    #del_table(db,table)