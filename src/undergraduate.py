from bs4 import (BeautifulSoup)
import urllib.request
from urllib.parse import urljoin #提供urljoin方法，便于处理动态链接，防止出现多次斜杠，并且防止多个域名
from urllib.error import HTTPError
import re
import os
#常量
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
url_Undergraduate="https://www.bkjx.sdu.edu.cn/"

#函数

def auto_mkdir(path):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)

def divContentProcess(divContent,category,rows):
    noticeItem = divContent.find_all("div",class_=["leftNews","leftNews1"]) #用class_参数寻找符合其中一个class的元素
    for item in noticeItem:
        itemTime = item.find("div",attrs={"style":"float:right;"}).getText()
        formattedItemTime = re.sub(r"\[|\]","",itemTime)
        itemDiv = item.find("a") #原本是寻找class="lastestnews"的，但是发现院内信息没这个class，而且itemDiv内只有一个a标签，故摆烂，直接找a
        itemHref = itemDiv.get('href')
        if (not re.search(r'http',itemHref)):     #处理动态链接，匹配是否有http字段判断是否为动态链接，也可以用上面str的startswith方法
            itemHref= urljoin(url_Undergraduate,itemHref)
        itemText = itemDiv.get('title')
        noticeFileGet(itemHref,category) # 爬取通知内容
        rows.append([formattedItemTime,itemText,itemHref])

# 爬取各个通知的内容
def noticeFileGet(url_notice,category): 
    requestNotice = urllib.request.Request(url=url_notice, headers=header)
    try: # 防止页面不存在(404)等异常
        page_notice = urllib.request.urlopen(requestNotice)    
        soup_notice = BeautifulSoup(page_notice,"html.parser")
        notice = soup_notice.find("form",attrs={"name":"_newscontent_fromname"})
        if notice==None: #防止通知内容无权限获取
            return "no notice existing"
        # 处理动态链接，替换为静态链接(包括附件、图片) 其中script由于无法加载，直接开摆清除
        for tag_a in notice.find_all('a',href=True): #href有内容即为True
            href = tag_a['href']
            if not href.startswith('http'):
                tag_a['href'] = urljoin(url_Undergraduate,href)
        for tag_script in notice.find_all('script'):
            tag_script.decompose()
        for tag_img in notice.find_all('img',src=True):
            src_img = tag_img['src']
            if not href.startswith('http'):
                tag_img['src'] = urljoin(url_Undergraduate,src_img)
        # Title get
        titleDiv = notice.find("div",attrs={"id":"newsTitle"})
        if (titleDiv):# 国际事务部的notice存储不大一样(h2)，做个判断
            titleText = titleDiv.find("div").getText()
        else :
            titleText = notice.find("h2").getText() 
        noticeHTML = notice.prettify() #转为str的同时，格式化HTML 已经处理了markdown识别空格导致转成代码块的问题.
        noticeHTML_noCR = re.sub(r"\n(.*?点击次数)",r"\1",noticeHTML) #用括号创建捕获组，\1代替捕获组，以此将捕获组前的\n去除
        path=r"notices/"+"本科生院/"+category+"/"+titleText +".md"
        auto_mkdir(path)
        with open(path,"w",encoding="utf-8-sig") as noticeText:
            noticeText.write(noticeHTML_noCR) #write需要一个str，而bs4存储的类型是tag，需要转成str
    except HTTPError: #略过404等错误
        return None

def spideUG(rows):

    requestWebsite = urllib.request.Request(url=url_Undergraduate,headers=header)
    page = urllib.request.urlopen(requestWebsite)
    soup = BeautifulSoup(page,"html.parser")
    noticeList =soup.find_all("div", attrs={"class":"gg-content"})
    rows.append(["工作通知:"])
    divContentProcess(noticeList[0],"工作通知",rows)
    rows.append(["教学快讯:"])
    divContentProcess(noticeList[1],"教学快讯",rows)
    rows.append(["公示公告:"])
    divContentProcess(noticeList[2],"公示公告",rows)
    rows.append(["院内信息:","注:院内信息访问需要登录教职工账号，无法爬取内容"])
    divContentProcess(noticeList[3],"院内信息",rows)
    

if __name__=="__main__":
    urlTest = "https://www.bkjx.sdu.edu.cn/info/1011/37124.htm"
    noticeFileGet(urlTest,"test")