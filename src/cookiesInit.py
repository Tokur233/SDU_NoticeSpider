from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import time

def getAttachmentCookie(url):
    driver = webdriver.Chrome()  
    driver.get(url)
    captcha_img = driver.find_element(By.ID, 'codeimg')  
    captcha_img.screenshot('captcha.png')
    captcha_code = pytesseract.image_to_string(Image.open('captcha.png')).strip()
    # print("Captcha code:", captcha_code)
    captcha_input = driver.find_element(By.ID, 'codeValue')  
    captcha_input.send_keys(captcha_code)
    confirm_button = driver.find_element(By.XPATH, "//input[@type='button' and @value='确 定']")
    confirm_button.click()
    cookies = driver.get_cookies()
    driver.quit()
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    # print("Cookies obtained:", cookie_dict)
    return cookie_dict

def validCookiesInit(): #此处仅初始化3个网站的有效cookies，即本科生院、国际事务部、青春山大这三个网站的有效附件cookie
    AttachmentURL_UG="https://www.bkjx.sdu.edu.cn/system/_content/download.jsp?urltype=news.DownloadAttachUrl&owner=1348324972&wbfileid=14861131"
    AttachmentURL_IPO="https://www.ipo.sdu.edu.cn/system/_content/download.jsp?urltype=news.DownloadAttachUrl&owner=1752217552&wbfileid=14865944"
    AttachmentURL_youth = "https://www.youth.sdu.edu.cn/system/_content/download.jsp?urltype=news.DownloadAttachUrl&owner=1775115926&wbfileid=14867394"
    cookies_UG = getAttachmentCookie(AttachmentURL_UG)
    cookies_IPO = getAttachmentCookie(AttachmentURL_IPO)
    cookies_youth = getAttachmentCookie(AttachmentURL_youth)
    cookiesMatchDict = {"www.bkjx.sdu.edu.cn":cookies_UG,"www.ipo.sdu.edu.cn":cookies_IPO,"www.youth.sdu.edu.cn":cookies_youth}
    return cookiesMatchDict

if __name__ =="__main__":
    cDict = validCookiesInit()
    print(cDict)
else :
    validCookiesDict = validCookiesInit()
    print(validCookiesDict)