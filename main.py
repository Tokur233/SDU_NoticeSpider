# from bs4 import (BeautifulSoup)
# import urllib.request
import csv
import re
import time
import os

#模块化
# import SDUMath 

# import SDUComputerScience
# import SDUStudentOnline

#常量
url_Undergraduate="https://www.bkjx.sdu.edu.cn/"
url_StudentOnline="https://online.sdu.edu.cn/"
url_ComputerScience="https://www.cs.sdu.edu.cn/"
url_Math="https://www.math.sdu.edu.cn/"
localtime = time.strftime("%Y-%m-%d", time.localtime())

#函数
def targetMatch(i,rows):
    match i:
        case 1:
            sources.append("计科本科院")
            
            pass
        case 2:
            sources.append("本科生院")
            undergraduate.spideUG(rows)
        case 3:
            sources.append("学生在线")
            pass
        case 4:
            sources.append("数学本科院")
            pass
        case 5:
            sources.append("青春山大")
            pass

print("请选择你的攻击网站(bushi):")
print("[1]山大计科本科院(未完成)")
print("[2]山大本科生院")
print("[3]山大学生在线(未完成)")
print("[4]山大数学本科院(未完成)")
print("[5]青春山大")
print("按你需要顺序填入数字，可以不分割或随便分割")
#处理成单数字数组，并匹配对应source
target=input()
targets = re.findall(r'\d',target)
sources=[]
rows =[[]]
import src.undergraduate as undergraduate #导入undergraduate和general 并初始化cookies init
for i in targets:
    i=int(i)
    targetMatch(i,rows)
source = ",".join(sources) #用逗号分割，将sources元素并放在一起
rows.insert(0,["爬取时间:"+localtime,"爬取来源:"+source])
if not os.path.exists("results"):
    os.makedirs("results")
with open(r"results/"+source+str(localtime)+".csv","w",newline="",encoding="utf-8-sig") as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(rows)


# TODO: 多网站、网页内容获取