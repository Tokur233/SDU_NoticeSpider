import os
import re
from bs4 import BeautifulSoup
#附件下载
import requests
from selenium import webdriver
from io import BytesIO
import time
from PIL import Image
import pytesseract

def auto_mkdir(path):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)

def getAttachment(url,path):
    pass

def getImage(page,path):
    pass

if __name__ == "__main__":
    #driver = webdriver.Chrome()
    url_testAttachment = "https://www.bkjx.sdu.edu.cn/system/_content/download.jsp?urltype=news.DownloadAttachUrl&owner=1348324972&wbfileid=14860069"
    url_testCaptcha = "https://www.bkjx.sdu.edu.cn/system/resource/js/filedownload/createimage.jsp?randnum=1730559877567"
    codeValue =1
    url_download = url_testAttachment +"&codeValue="+codeValue
    response = requests.get(url_testCaptcha)
    image = Image.open(BytesIO(response.content))
    captcha_text = pytesseract.image_to_string(image, config='--psm 8')
    print(f'Captcha recognized: {captcha_text}')
    time.sleep(3)
    #driver.quit()