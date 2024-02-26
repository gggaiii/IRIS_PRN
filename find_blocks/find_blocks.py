from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from bs4 import BeautifulSoup
import time

file_path = 'D:/JLL/Test/IRIS_PRN/find_blocks/html.txt'  # 替换为你的文本文件路径

# 打开文本文件
with open(file_path, 'r', encoding='utf-8') as file:
    text_content = file.read()

html = text_content

def parse_tables(html):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', {'class': 'generalTbl'})  # 找到所有类名为generalTbl的表格
    for i, table in enumerate(tables):
        rows = table.find_all('tr')  # 找到所有的行
        row_count = len(rows)
        col_count = max(len(row.find_all(['th', 'td'])) for row in rows)  # 找到列数
        print(f"表格 {i+1}：行数：{row_count}, 列数：{col_count}")

parse_tables(html)