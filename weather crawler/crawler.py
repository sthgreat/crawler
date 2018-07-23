import requests
import re
from bs4 import BeautifulSoup
import bs4
import os

def get(url):
    try:
        r = requests.get(url, timeout=300)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("1")

def getonemonth(ulist, html):
    html1 = re.sub('<b>|</b>|<a\s.*\s.*>|</a>|\r|\n', '', html)
    soup = BeautifulSoup(html1, "lxml")
    for tr in soup.find('table').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            a1 = re.sub(' ', '', tds[0].string)
            a2 = re.sub(' ', '', tds[1].string)
            a3 = re.sub(' ', '', tds[2].string)
            a4 = re.sub(' ', '', tds[3].string)
            ulist.append([a1, a2, a3, a4])

def text_save(path1, path2, content, num ,mode='a'):
    # Try to save a list variable in txt file.
    mkdir(path1)
    file = open(path2, mode)
    for i in range(num):
        u = content[i]
        file.write("{:^15}\t{:^15}\t{:^15}\t{:^15}".format(u[0], u[1], u[2], u[3]) + '\n')
    file.close()


def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
    else:
        return False

def main():
    # 查询城市
    city = input("所要查询请输入城市拼音：")
    # 起始年份
    startyaer = input("请输入起始年份：")
    year = []
    # num为年份跨度
    num = int(input("请输入年份跨度（数字）："))
    count = 0
    for i in range(num):
        startyears = str(int(startyaer) + i)
        year.append(startyears)
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    list = []
    for m in range(0, num):
        for n in range(0, 12):
            url = 'http://www.tianqihoubao.com/lishi/' + city + '/month/' + year[m] + months[n] + '.html'
            path1 = "D:/pics/kunming/" + year[m] + "年/"
            path2 = "D:/pics/kunming/" + year[m] + "年/" + months[n] + "月" + ".txt"
            html = get(url)
            list = []
            getonemonth(list, html)
            text_save(path1, path2, list, len(list))
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count * 100 / (num * 12)), end="")

main()
