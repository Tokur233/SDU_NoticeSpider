from bs4 import (BeautifulSoup)
from urllib.error import HTTPError
import re
import src.general as general
#常量
from src.constant import URL_YOUTH
SOURCE = "青春山大"
def CrawlYouth(rows):
    soup = general.getPage(URL_YOUTH)
    noticeList = soup.find("ul",attrs={"class":"tdate-list"})
    fileList = soup.find("ul",attrs={"class":"bg-lists"})
    followList = soup.find("ul",attrs={"class":"gz-lists"})
    rows.append(["重要通知:"])
    contentProcess(noticeList,"重要通知",rows)
    rows.append(["办公文件:"])
    contentProcess(fileList,"办公文件",rows)
    rows.append(["最新关注:"])
    contentProcess(followList,"最新关注",rows)

def contentProcess(List,category,rows):
    items = List.find_all("li")
    for item in items:
        itemHref = general.dynamicRefProcess(URL_YOUTH,item.find("a")['href'])
        try:
            itemPage = general.getPage(itemHref)
            form = itemPage.find("form",attrs={"name":"_newscontent_fromname"})
            if form == None:
                continue
        except HTTPError:
            continue
        itemDate = form.find("span").getText()
        itemTitle = form.find("h3").getText()
        rows.append([itemDate,itemTitle,itemHref])
        general.noticeGet(itemHref,form,SOURCE,category)
