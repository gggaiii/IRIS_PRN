from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from bs4 import BeautifulSoup
import time

path = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
s = Service(executable_path=path)
# 创建Chrome浏览器实例
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=s, options=options)

A = []
B = []

file_path = 'D:/JLL/Test/IRIS_PRN/find_blocks/html.txt'  # 替换为你的文本文件路径

# 打开文本文件
with open(file_path, 'r', encoding='utf-8') as file:
    text_content = file.read()

html = text_content
soup = BeautifulSoup(html, 'html.parser')
tree = etree.HTML(html)

# 使用 BeautifulSoup 解析页面源码
soup_block_page = BeautifulSoup(html, 'html.parser')
tables = soup_block_page.find_all('table', {'class': 'generalTbl'})  # 找到所有类名为generalTbl的表格

# print(tables[0])

rows = tables[0].find_all('tr')  # 找到所有的行
row_count = len(rows)
col_count = max(len(row2.find_all(['th', 'td'])) for row2 in rows)  # 找到列数
print(f"表格行数：{row_count}, 列数：{col_count}")

for index1 in range(2, row_count + 1):
    for index2 in range(1, col_count + 1):
        real_block_path = '//*[@id="multiSelect"]/tr[' + str(index1) + ']/td[' + str(index2) + ']'

        cells = tree.xpath(real_block_path)  # 使用xpath找到所有的单元格

        for i, cell in enumerate(cells):
            content_tree = cell.text
            # print(content_tree)

            if content_tree is not None:
                content_tree = content_tree.strip()  # 去除两边的空白字符
            if not (content_tree == "&nbsp;" or content_tree == ""):
                element_room = driver.find_element('xpath', real_block_path)
                # 模拟鼠标移动到元素上并点击
                actions = ActionChains(driver)
                actions.move_to_element(element_room).click().perform()

                # 获取网站的HTML内容
                html_room_page = driver.page_source

                # 使用 BeautifulSoup 解析页面源码
                soup = BeautifulSoup(html_room_page, 'html.parser')
                tbody = soup.find_all('tbody')[1]

                # 提取数据
                records = []
                status = []
                for row in tbody.select('tr'):
                    link = row.find('a')
                    if link:
                        PRN = link.text.strip().replace('(', '').replace(')',
                                                                         '')  # 去除括号和空格  # 提取 <a> 元素的文本内容并去除首尾空格
                        records.append(PRN)

                    link1 = row.find('span')
                    if link1:
                        STA = link1.text.strip().replace('(', '').replace(')',
                                                                          '')  # 去除括号和空格  # 提取 <a> 元素的文本内容并去除首尾空格
                        if (STA == ''):
                            STA = 'Valid'
                        status.append(STA)

                A.extend(records)
                B.extend(status)