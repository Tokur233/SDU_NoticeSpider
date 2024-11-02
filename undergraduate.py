from bs4 import (BeautifulSoup)
import urllib.request
import re

url_Undergraduate="https://www.bkjx.sdu.edu.cn/"
def divContentProcess(divContent,rows):
    noticeItem = divContent.find_all("div",class_=["leftNews","leftNews1"]) #用class_参数寻找符合其中一个class的元素
    for item in noticeItem:
        itemTime = item.find("div",attrs={"style":"float:right;"}).getText()
        formattedItemTime = re.sub(r"\[|\]","",itemTime)
        itemDiv = item.find("a") #原本是寻找class="lastestnews"的，但是发现院内信息没这个class，而且itemDiv内只有一个a标签，故摆烂，直接找a
        itemHref = itemDiv.get('href')
        if (not re.search(r'http',itemHref)):     #处理动态链接，匹配是否有http字段判断是否为动态链接
            itemHref= url_Undergraduate +itemHref
        itemText = itemDiv.get('title')
        rows.append([formattedItemTime,itemText,itemHref])
def spideUG(rows):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }
    request = urllib.request.Request(url=url_Undergraduate,headers=header)
    page = urllib.request.urlopen(request)
    soup = BeautifulSoup(page,"html.parser")
    notice =soup.find_all("div", attrs={"class":"gg-content"})
    rows.append(["工作通知:"])
    divContentProcess(notice[0],rows)
    rows.append(["教学快讯:"])
    divContentProcess(notice[1],rows)
    rows.append(["公示公告:"])
    divContentProcess(notice[2],rows)
    rows.append(["院内信息:","注:院内信息访问需要登录教职工账号"])
    divContentProcess(notice[3],rows)
    

