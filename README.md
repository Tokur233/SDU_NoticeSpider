## 进度

目前只做了本科生院的最新几个通知的文本、图片、附件的爬取，旧通知暂时不爬。

## 环境依赖

__依赖库：__csv,bs4,urllib,requests,PIL(pillow),pytesseract,selenium
均可用pip install下载，但是需要注意的是，pytesseract的OCR需要额外在官网下载，并添加到环境变量里，selenium需要搭配ChromeDriver。

__额外依赖：__ChromeDriver

需要下载后送到环境变量里。

## 使用方法

打开'main.py'即可使用，因为只做了本科生院，所以只能选2，相当的方便（赞赏）.

爬取结果将在'results'和'notices'文件夹展示。'results'是爬取通知的概述，'notices'包含通知的正文(可正常显示图片)、图片、附件。
