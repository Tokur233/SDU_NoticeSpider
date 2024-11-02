## 进度

目前只做了本科生院的最新几个通知的文本、图片、附件的爬取，旧通知暂时不爬。

## 环境依赖

**依赖库：**csv,bs4,urllib,requests,PIL(pillow),pytesseract,selenium
均可用pip install下载，但是需要注意的是，pytesseract的OCR需要额外在官网下载，并添加到环境变量里，selenium需要搭配ChromeDriver。

**额外依赖：**ChromeDriver

需要下载后送到环境变量里。

## 使用方法

打开main.py即可使用，因为只做了本科生院，所以只能选2，相当的方便（赞赏）.

爬取结果将在results和notices文件夹展示。results是爬取通知的概述，notices包含通知的正文(可正常显示图片)、图片、附件。
