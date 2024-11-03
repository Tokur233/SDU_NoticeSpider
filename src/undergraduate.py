from bs4 import (BeautifulSoup)
import urllib.request
from urllib.parse import urljoin #提供urljoin方法，便于处理动态链接，防止出现多次斜杠，并且防止多个域名,urlparse用于解析url，其中.netloc为域名
from urllib.error import HTTPError
import re
import src.general as general
#常量
from src.constant import URL_UG,HEADER
SOURCE = "本科生院"
#函数

def crawlUG(rows):
    soup = general.getPage(URL_UG)
    noticeList =soup.find_all("div", attrs={"class":"gg-content"})
    rows.append(["工作通知:"])
    divContentProcess(noticeList[0],"工作通知",rows)
    rows.append(["教学快讯:"])
    divContentProcess(noticeList[1],"教学快讯",rows)
    rows.append(["公示公告:"])
    divContentProcess(noticeList[2],"公示公告",rows)
    rows.append(["院内信息:","注:院内信息访问需要登录教职工账号，无法爬取内容"])
    divContentProcess(noticeList[3],"院内信息",rows)

def divContentProcess(divContent,category,rows):
    noticeItem = divContent.find_all("div",class_=["leftNews","leftNews1"]) #用class_参数寻找符合其中一个class的元素
    for item in noticeItem:
        itemTime = item.find("div",attrs={"style":"float:right;"}).getText()
        formattedItemTime = re.sub(r"\[|\]","",itemTime)
        itemDiv = item.find("a") #原本是寻找class="lastestnews"的，但是发现院内信息没这个class，而且itemDiv内只有一个a标签，故摆烂，直接找a
        itemHref = itemDiv.get('href')
        itemHref = general.dynamicRefProcess(URL_UG,itemHref)
        itemText = itemDiv.get('title')
        rows.append([formattedItemTime,itemText,itemHref]) #这个部分和上一行按网站的设定来，可以来自于网站通知item，也可以来自于通知page的title
        # notice page处理
        requestNotice = urllib.request.Request(url=itemHref, headers=HEADER)
        try: # 防止页面不存在(404)等异常
            page_notice = urllib.request.urlopen(requestNotice)    
            soup_notice = BeautifulSoup(page_notice,"html.parser")
            notice = soup_notice.find("form",attrs={"name":"_newscontent_fromname"})
            if notice==None: #防止通知内容无权限获取
                continue
        except HTTPError:
            continue
        general.noticeGet(itemHref,notice,SOURCE,category)# 爬取通知内容



if __name__=="__main__":
    pass