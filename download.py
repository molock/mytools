# -*- coding: utf-8 -*-
'''
Created on 2013-1-23

@author: Administrator
'''
import urllib2,re,os
import MyHTMLParser

class HTMLImgParser(MyHTMLParser.HTMLParser):
    def __init__(self):
        self.starturl = ""
        self.webcontent = ""
        self.imglinks = []
        self.hreflinks = []
        self.reset()

    #只找带img tag的元素
    def handle_startendtag(self,tag,attrs):
            if tag == 'img':
                for attr in attrs:
                    if attr[0]=='src':
                        if re.match('[\bhttp\w*\b]',attr[1]):
                            print "Image link:", attr[1]
                            link = attr[1]
                            l = re.split('[\/]', link)
                            filename = l[-1]
                            self.imglinks.append((filename,link))

    #只找href链接元素
    def handle_starttag(self,tag,attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0]=='href':
                    if re.match(r"http://",attr[1]):
                        self.hreflinks.append(attr[1])
                        print "save link:",attr[1]
                    else :
                        baseurl = re.split('[\/]+',self.starturl)
                        url = r"http://" + baseurl[1] + attr[1]
                        self.hreflinks.append(url)
                        print "save link:", url

    def feedurl(self,url):
        self.starturl = url
        cs = urllib2.urlopen(self.starturl)
        self.webcontent = cs.read()
        cs.close()
        self.feed(self.webcontent)

    def getsourcelinks(self):
        return self.imglinks

    def gethreflinks(self):
        return self.hreflinks

class Downloader:
    '''
            创建下载器需要给定下载类型和开始下载的网址
            下载类型：0：图片     1：网页
    '''
    def __init__(self,downloadtype,starturl):
        self.CONFIG = "downloadconfig.txt"
        self.defultdownloaddir = ('D:\\htmldownload\\') #没有指定config文件的时候就用这个
        self.downloadtype = downloadtype
        self.starturl = starturl
        self.savedir = ""
        self.depth = 0 #每下载完一个网页即增加一个深度
        self.maxdepth = 1
        self.currentpage = starturl #当前下载的网页地址
        self.hreflinks = [[starturl]]
        #创建对象后就获取config文件
        self.getconfig()

    #如果没有配置文件，就按默认设置在本文件夹创建一个
    def getconfig(self):
        try:
            f = open(self.CONFIG,'r')
            for index,line in enumerate(f.readlines()):
                if index == 0:
                    self.savedir = re.sub(r'\n','',line)
                f.close()
        except IOError:
            if not os.path.exists(self.CONFIG):
                f = open(self.CONFIG,'w')
                f.write(self.defultdownloaddir)
                self.savedir = self.defultdownloaddir

    def download(self):
        if self.downloadtype == 0:
            parser = HTMLImgParser()
        while(self.depth < self.maxdepth):
            print self.hreflinks
            parser.feedurl(self.hreflinks[self.depth].pop())
            sourcelinks = parser.getsourcelinks()
            try:
                self.hreflinks[self.depth + 1].extend(parser.gethreflinks())
            except IndexError:
                self.hreflinks.append([])
                self.hreflinks[self.depth + 1].extend(parser.gethreflinks())

            if not self.hreflinks[self.depth]:
                self.depth = self.depth + 1
                print "depth" ,self.depth,"is done!"

            for cell in sourcelinks:
                filename = cell[0]
                try:
                    content = urllib2.urlopen(cell[1])
                    source = content.read()
                    content.close()
                    if not os.path.exists(self.savedir):
                        os.mkdir(self.savedir)
                    if os.path.exists(self.savedir + filename):
                        filename = "new_" + filename
                    f = open(self.savedir + filename,'w+b')
                    f.write(source)
                    f.close()
                    print self.savedir + filename ,"has being downloaded!"
                except Exception:
                    continue




if __name__ == "__main__":
    dl = Downloader(0,"http://99.99btgc.info/p2p/01/13-01-27-20-03-24.html")
    dl.download()

