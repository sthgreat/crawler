from selenium import webdriver
import selenium.webdriver.support.ui as ui
from bs4 import BeautifulSoup


def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
    else:
        return False


def save(search_word,papername_li,abstract_li,keyword_li):
    mkdir("./data/" + search_word)
    for num in range(len(abstract_li)):
        with open("./data/" +search_word + "/" + papername_li[num] +".txt", 'a', encoding='utf-8') as f:
            f.write("摘要：" + abstract_li[num] + '\n')
            f.write("关键字：")
            for i in range(len(keyword_li[num])):
                if i != len(keyword_li[num]):
                    f.write(keyword_li[num][i] + "，")
                else:
                    f.write(keyword_li[num][i])


def get_information(html_page, papername_li, abstract_li, keyword_li):
    soup = BeautifulSoup(html_page, "html.parser")
    paper_name = soup.find('title').text
    abstract = soup.find_all(id=["ChDivSummary"])  # 寻找摘要
    keyword = soup.find_all(id=["ChDivKeyWord"])[0].find_all('a')  # 关键字
    for i in abstract:
        abstract_li.append(i.text)
    li = []
    for word in keyword:
        li.append(word.text)
    papername_li.append(paper_name)
    keyword_li.append(li)


def circle(url, search_word, control, search_number):
    papername_li = []
    abstract_li = []
    keyword_li = []

    css_selector_front = "#ctl00 > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child("
    css_selector_back = ") > td:nth-child(2) > a"

    wd = webdriver.Chrome()
    wd.get(url)
    wd.find_element_by_css_selector("#txt_1_value1").send_keys(search_word)
    wd.find_element_by_css_selector("#btnSearch").click()

    first_window_handle = wd.current_window_handle  # 记录第一层窗口的句柄
    for i in range(2, search_number + 2):
        css_selector = css_selector_front + str(i) + css_selector_back
        wd.switch_to.frame("iframeResult")  # 向页面中的frame结构转移
        try:
            wait = ui.WebDriverWait(wd, 10)  # 等待元素加载
            wait.until(lambda driver: driver.find_element_by_css_selector(css_selector))  # 等待元素加载
            wd.find_element_by_css_selector(css_selector).click()
            wd.switch_to.default_content()
        except:
            continue

        handles = wd.window_handles  #记录所有窗口句柄
        # print(handles)
        # print(type(handles))
        for handle in handles:  # 转移句柄
            if handle != first_window_handle:
                wd.switch_to.window(handle)

        html = wd.page_source
        get_information(html,papername_li,abstract_li,keyword_li)  # 摘要与文章名获取
        if control == 1:  # 控制页面下载
            pass

        wd.close()  # 关闭二级页面
        wd.switch_to.window(first_window_handle)  # 转移句柄至一级页面

    save(search_word, papername_li, abstract_li, keyword_li)


if __name__ == "__main__":
    search_number = 1  # 获取搜索结果的前n个
    search_word = "电容型设备"  # 搜索关键字
    url = "http://epub.cnki.net/kns/default.htm"
    circle(url, search_word, 1, search_number)
