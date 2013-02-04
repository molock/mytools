#coding=utf-8
from openpyxl import load_workbook
import os

defultpath = 'E:\\工作\\works'

filelist = []
# wb = load_workbook(filename = r'empty_book.xlsx')


for root,dir,files in os.walk(defultpath):
    for name in files:
        filepath = os.path.join(root,name)
        filepath = filepath.decode(encoding='GB2312').encode(encoding='utf-8')
        print filepath
        filelist.append(filepath)

print filelist