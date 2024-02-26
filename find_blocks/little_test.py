from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from bs4 import BeautifulSoup
import time
from lxml import etree

file_path = 'D:/JLL/Test/IRIS_PRN/find_blocks/html.txt'  # 替换为你的文本文件路径
# 打开文本文件
with open(file_path, 'r', encoding='utf-8') as file:
    text_content = file.read()

html = text_content
tree = etree.HTML(html)

# 使用 BeautifulSoup 解析页面源码
soup_block_page = BeautifulSoup(html, 'html.parser')

tables = soup_block_page.find_all('table', {'class': 'generalTbl'})  # 找到所有类名为generalTbl的表格

for j, block_table in enumerate(tables):
    rows1 = block_table.find_all('tr')  # 找到所有的行
    row_count1 = len(rows1)
    col_count1 = max(len(row2.find_all(['th', 'td'])) for row2 in rows1)  # 找到列数
    print(f"表格 {j + 1}：行数：{row_count1}, 列数：{col_count1}")

    for index1 in range(2, row_count1+1):
        for index2 in range(1, col_count1+1):
            real_block_path = '//*[@id="multiSelect"]/tr[' + str(index1) + ']/td[' + str(index2) + ']'

            cells = tree.xpath(real_block_path)  # 使用xpath找到所有的单元格
            for i, cell in enumerate(cells):
                content = cell.text
                if content is not None:
                    content = content.strip()  # 去除两边的空白字符
                if content == "&nbsp;" or content == "":
                    print(f"单元格 {i + 1} 是空的")
                else:
                    print(f"单元格 {i + 1} 的内容是：{content}")