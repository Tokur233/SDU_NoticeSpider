from bs4 import (BeautifulSoup)
import urllib.request
from urllib.parse import urljoin #提供urljoin方法，便于处理动态链接，防止出现多次斜杠，并且防止多个域名,urlparse用于解析url，其中.netloc为域名
from urllib.error import HTTPError
import re
import src.general as general
#常量
from src.constant import URL_CS
SOURCE = "计科学院"

def crawlCSUG(rows):
    soup = general.getPage(URL_CS)
    noticesList = soup.find_all("ul",attrs={"class":"dh"}) #计科后方3个栏的条目太过时了，本来想只爬学院新闻、本科通知、研究生通知，但是我们都爬一下吧
    rows.append(["学院新闻:"])
    newsProcess(noticesList[0],"学院新闻",rows)
    rows.append(["学院公告:"])
    noticeProcess(noticesList[1],"学院公告",rows)
    rows.append(["学术报告:"])
    reportProcess(noticesList[2],"学术报告",rows)
    rows.append(["科技简迅:"])
    noticeProcess(noticesList[3],"科技简讯",rows)
    rows.append(["本科公告:"])
    noticeProcess(noticesList[4],"本科公告",rows)
    rows.append(["研究生公告:"])
    noticeProcess(noticesList[5],"研究生公告",rows)

def newsProcess(newsList,category,rows):
    newsItems = newsList.find_all("li")
    for newsItem in newsItems:
        dateDiv = newsItem.find("div",attrs={"class":"tz-date"})
        day = dateDiv.find("span").getText()
        year_month = re.findall(r"\d{4}-\d{2}",str(dateDiv))[0]
        newsDate = year_month +"-"+ day
        newsTitle = newsItem.find("a").get('title')
        aTagHref = newsItem.find("a").get('href')
        # if aTagHref.startswith("http"):
        #     newsHref = aTagHref
        # else:
        #     newsHref = urljoin(URL_CS,aTagHref)
        newsHref = general.dynamicRefProcess(URL_CS,aTagHref)
        rows.append([newsDate,newsTitle,newsHref])
        try:
            newsPage = general.getPage(newsHref)
            news = newsPage.find("form",attrs={"name":"_newscontent_fromname"})
            if news == None:
                continue
        except HTTPError:
            continue
        general.noticeGet(newsHref,news,SOURCE,category)

def noticeProcess(noticeList,category,rows):
    noticeItems = noticeList.find_all("li")
    for noticeItem in noticeItems:
        noticeDate = noticeItem.find("span",attrs={"class":"dates"}).getText()
        noticeTitle = noticeItem.find("a").get('title')
        aTagHref = noticeItem.find("a").get('href')
        # if aTagHref.startswith("http"):
        #     noticeHref = aTagHref
        # else:
        #     noticeHref = urljoin(URL_CS,aTagHref)
        noticeHref = general.dynamicRefProcess(URL_CS,aTagHref)
        rows.append([noticeDate,noticeTitle,noticeHref])
        try:
            noticePage = general.getPage(noticeHref)
            notice = noticePage.find("form",attrs={"name":"_newscontent_fromname"})
            if notice == None:
                continue
        except HTTPError:
            continue
        general.noticeGet(noticeHref,notice,SOURCE,category)

def reportProcess(reportList,category,rows):
    reportItems = reportList.find_all("li")
    for reportItem in reportItems:
        reportTime = reportItem.find("p",attrs={"class":"time"})
        reportAddress = reportItem.find("p",attrs={"class":"adress"})
        reportTitle = reportItem.find("a").get('title')
        aTagHref = reportItem.find("a").get('href')
        # if aTagHref.startswith("http"):
        #     reportHref = aTagHref
        # else:
        #     reportHref = urljoin(URL_CS,aTagHref)
        reportHref = general.dynamicRefProcess(URL_CS,aTagHref)
        rows.append([reportTime,reportAddress,reportTitle,reportHref])
        try:
            reportPage = general.getPage(reportHref)
            report = reportPage.find("form",attrs={"name":"_newscontent_fromname"})
            if report == None:
                continue
        except HTTPError:
            continue
        general.noticeGet(reportHref,report,SOURCE,category)
if __name__ == "__main__":
    rows=[[]]