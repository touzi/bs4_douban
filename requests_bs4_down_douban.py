# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
import os, urllib2, urllib
import time

def tieba_url():
    print u'请输入想要去的豆瓣小组：'
    name = raw_input('如:haixiuzu>')
    # 创建主文件夹//
    path = os.getcwd()
    path = unicode(path.decode('gbk'))          #!# 将win路径转化为unicode
    path = os.path.join(path,u'爬虫实验')
    tieba = unicode(name.decode('gbk'))         #!#  unicode,之前老报错 
    pathr = os.path.join(path,tieba) 
    if not os.path.isdir(pathr):
        os.mkdir(pathr)
    url = 'http://www.douban.com/group/%s/discussion?start=' % name
    urlr = urllib.quote(url,':/?=&')
    #print url
    return (urlr, pathr)

def page_change(page,url):
        url= '%s%d' %(url,page)          #!# 连接字符串和整型的方法，好牛！！
        print '==>%s' % url
        content = urllib2.urlopen(url).read()
        #print 'content=>%s' % content
        soup = BeautifulSoup(content)
        #print soup.find_all('td',attrs={"class": "title"})
        my_tiezi = soup.find_all('td',attrs={"class": "title"})
        #print my_tiezi
        return my_tiezi
    
# 创建从贴吧页面获取帖子网址的函数：
def tieba_find_link(my_tiezi):   
        flinks = []
        titles = []
        
        for tiezi in my_tiezi:

                link = tiezi.a.get('href')
                #flink = 'http://tieba.baidu.com' + link + '?see_lz=1' #只看LZ不止一页怎么搞，总页数怎么确定
                flink = link
                #print 'flink>%s' % flink
                title = tiezi.a.string.encode('gbk','ignore')
                #print 'flink>%s' % title
                flinks.append(flink)
                titles.append(title)
                return (flinks, titles)                            # 第一次遇到，搜索了，发现了元组这个好东西

            
# 创建从帖子本身获取楼主照片的函数：
def get_img(flinks,titles,path):
    
    for i in range(len(flinks)):					# 巧妙的解决了同时解包元组的问题
        flink = flinks[i]
        title = titles[i]
        #print 'flink>%s' % flink
        content = urllib2.urlopen(flink).read()
        #print 'content>%s' % content
        soup = BeautifulSoup(content)
        ilinks = soup.find_all('img',attrs={"alt": "","class": "","title": "","width":"","height":""})
        #print 'ilinks>%s' % ilinks
#检测是否有图片，如果没图片，忽略该帖子//
        if ilinks == []:
                continue

        for ilink in ilinks:
            src = ilink.get('src')
            print u'准备下载图片，来自帖子'+ unicode(title.decode('gbk'))
            try:
                content = urllib2.urlopen(src,timeout=5).read()
            except:
                print u'请求超时，放弃下载此照片'
                continue
            print u'下载完毕'
#
            try:
                with open(path+'/'+src[-11:],'wb') as code:
                        code.write(content)
                print u'成功保存照片'
#print u'保存完毕'
            except:
                print u'估计是文件夹名字的问题，保存失败:'
                print path+'/'+src[-10:]

# 这是主函数：


def main(url,path,page=0):	
	p1 = page_change(page,url)
	#print 'p1=>%s' % p1
	(flinks,titles) = tieba_find_link(p1)
	get_img(flinks,titles,path)
	page = int(page) + 25
	print u'开始抓取下一页'
	print '-'* 40
	main(url,path,page)        #之前这个顺序弄错了，老是报错。

(url, path) = tieba_url()
main(url,path)
