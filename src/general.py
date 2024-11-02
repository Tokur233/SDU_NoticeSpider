import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse,urljoin
#附件下载
import requests
from src.cookiesInit import validCookiesDict #导入并初始化validCookiesDict

#常量
from src.constant import HEADER

def auto_mkdir(path):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)

def getImage(page,path):
    i = 1 #图片名计数
    for tag_img in page.find_all('img'):
        img_url = tag_img.get('src') #注：get方法返回的是str或None,可以捕获异常,而img['src']直接访问，如果空可能报错。但是我们懒着捕获异常
        if re.search(r"icon_|time3.png|liulan.png|go-back.png",img_url):
            continue
        img_response = requests.get(img_url)
        img_ext = os.path.splitext(img_url)[1] #splitext方法用于分割文件名，返回元组，第一个元素为文件名，第二个元素为扩展名
        imgPath = path + '/'+ str(i) + img_ext
        auto_mkdir(imgPath)
        with open(imgPath,'wb') as img:
            img.write(img_response.content)
        i= i+1
def noticeGet(url_notice,noticePage,source,category): #category指工作通知等类别，source指本科生院等来源
    # 处理动态链接，替换为静态链接(包括附件、图片) 其中script由于无法加载，直接开摆清除
    url_parse = urlparse(url_notice)
    domain = url_parse.scheme+"://"+url_parse.netloc  #传输协议protocol (scheme)加上域名domain (netloc)
    for tag_a in noticePage.find_all('a',href=True): #href有内容即为True
        href = tag_a['href']
        if not href.startswith('http'):
            tag_a['href'] = urljoin(domain,href)
    for tag_script in noticePage.find_all('script'):
        tag_script.decompose()
    for tag_img in noticePage.find_all('img',src=True):
        src_img = tag_img['src']
        if not href.startswith('http'):
            tag_img['src'] = urljoin(domain,src_img)
    # Title get
    titleDiv = noticePage.find("div",attrs={"id":"newsTitle"})
    if (titleDiv):# 国际事务部的notice存储不大一样(h2)，做个判断
        titleText = titleDiv.find("div").getText()
    elif(noticePage.find("h2")):
        titleText = noticePage.find("h2").getText() 
    else:
        titleText = noticePage.find("h3").getText()
    #下载图片
    path=r"notices/"+source+"/"+category+"/"
    getImage(noticePage,path+titleText)
    # 下载附件
    cookie = validCookiesDict[url_parse.netloc]
    attachmentList = noticePage.find_all('li')
    if attachmentList != None:
        for attachmentItem in attachmentList:
            attachmentTag_a = attachmentItem.find("a",href=True)
            attachmentHref = attachmentTag_a['href']
            attachmentName = attachmentTag_a.getText()
            attachment = requests.get(attachmentHref,headers=HEADER,cookies=cookie,allow_redirects=True)
            attachmentPath =path+titleText+'/'+attachmentName
            auto_mkdir(attachmentPath)
            with open(attachmentPath,'wb') as file:
                file.write(attachment.content)
    noticeHTML = noticePage.prettify() #转为str的同时，格式化HTML 已经处理了markdown识别空格导致转成代码块的问题.
    noticeHTML_noCR = re.sub(r"\n(.*?点击次数)",r"\1",noticeHTML) #用括号创建捕获组，\1代替捕获组，以此将捕获组前的\n去除
    filePath= path + titleText + ".md"
    auto_mkdir(filePath)
    with open(filePath,"w",encoding="utf-8-sig") as noticeText:
        noticeText.write(noticeHTML_noCR)



if __name__ == "__main__":
    test_fileURL = "https://www.baidu.com/robots.txt"
