from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from bs4 import BeautifulSoup
import time
from lxml import etree

path = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
s = Service(executable_path=path)
# 创建Chrome浏览器实例
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=s, options=options)

# 打开网页
# url = "https://www1.iris.gov.hk/eservices"
url = 'https://www1.iris.gov.hk/eservices'
driver.get(url)

# 模拟点击Search
element = driver.find_element('xpath', '//*[@id="menu1"]/a')
# 模拟鼠标移动到元素上并点击
actions = ActionChains(driver)
actions.move_to_element(element).click().perform()

# 模拟点击Search PRN
element1 = driver.find_element('id', 'menu1_2')
# 模拟鼠标移动到元素上并点击
actions = ActionChains(driver)
actions.move_to_element(element1).click().perform()

# 等待键盘输入回车，输入验证码后在浏览器点continue或enter，回到终端中输入Enter，浏览器会自动继续执行
input("请按回车键继续...")

# 定位输入框
input_element = driver.find_element('xpath', '//*[@id="SDevelopmentNameEng"]')
# 输入字符串
input_element.send_keys("WINNER BUILDING")

time.sleep(1)
# 在网站空白处模拟一次点击,以关闭下拉栏，暴露continue按钮
elementempty = driver.find_element('xpath', '//*[@id="zoomIn"]/i')
# 模拟鼠标移动到元素上并点击
actions = ActionChains(driver)
actions.move_to_element(elementempty).click().perform()

time.sleep(1)

# 模拟点击continue
element3 = driver.find_element('xpath', '//*[@id="continueButton"]')
# 模拟鼠标移动到元素上并点击
actions = ActionChains(driver)
actions.move_to_element(element3).click().perform()

# 获取网站的HTML内容
html_building_page = driver.page_source

# 使用 BeautifulSoup 解析页面源码
soup_building_page = BeautifulSoup(html_building_page, 'html.parser')

A = []
B = []

# tables = soup_building_page.find_all('table', {'class': 'generalTbl'})  # 找到所有类名为generalTbl的表格
tables = soup_building_page.find_all('table', {'class': 'generalTbl'})  # 找到所有类名为generalTbl的表格
for i, building_table in enumerate(tables):
    rows = building_table.find_all('tr')  # 找到所有的行
    row_count = len(rows)
    col_count = max(len(row.find_all(['th', 'td'])) for row in rows)  # 找到列数
    print(f"表格 {i+1}：行数：{row_count}, 列数：{col_count}")


    for index in range(2, 3):
        if i == 0:
            realpath = '//*[@id="multiSelect"]/tr[' + str(index) + ']/td[1]'
        else:
            realpath = '//*[@id="multiSelect' + str(i+1) + '"]/tr[' + str(index) + ']/td[1]'
        element_block = driver.find_element('xpath', realpath)
        # 模拟鼠标移动到元素上并点击
        actions = ActionChains(driver)
        actions.move_to_element(element_block).click().perform()

        # 获取网站的HTML内容
        html_block_page = driver.page_source
        tree = etree.HTML(html_block_page)

        # 使用 BeautifulSoup 解析页面源码
        soup_block_page = BeautifulSoup(html_block_page, 'html.parser')

        tables = soup_block_page.find_all('table', {'class': 'generalTbl'})  # 找到所有类名为generalTbl的表格

        for j, block_table in enumerate(tables):
            rows1 = block_table.find_all('tr')  # 找到所有的行
            first_cell = rows1[0].find('th')  # 找到第一行第一列的单元格
            content_column = first_cell.text.strip()  # 获取单元格的内容并去除两边的空白字符
            row_count1 = len(rows1)
            col_count1 = max(len(row2.find_all(['th', 'td'])) for row2 in rows1)  # 找到列数
            print(f"表格 {j + 1}：行数：{row_count1}, 列数：{col_count1}")

            if content_column == 'Flat':
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

                # 模拟点击back
                print('Search Ended for This Block')
                # 模拟点击back to bulidings
                element6 = driver.find_element('xpath',
                                                   '//*[@id="page-content"]/tbody/tr[1]/td[2]/table/tbody/tr/td/div/form/table[3]/tbody/tr[1]/td/a[2]')
                # 模拟鼠标移动到元素上并点击
                actions = ActionChains(driver)
                actions.move_to_element(element6).click().perform()

            else:
                for index1 in range(2, row_count1+1):
                    for index2 in range(1, col_count1+1):
                        real_block_path = '//*[@id="multiSelect"]/tr[' + str(index1) + ']/td[' + str(index2) + ']'

                        cells = tree.xpath(real_block_path)  # 使用xpath找到所有的单元格

                        for i, cell in enumerate(cells):
                            content_tree = cell.text
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

                                # 模拟点击back
                                if index1 == row_count1 & index2 == col_count1:
                                    print('Search Ended for This Block')
                                    # 模拟点击back to bulidings
                                    element6 = driver.find_element('xpath',
                                                                   '//*[@id="page-content"]/tbody/tr[1]/td[2]/table/tbody/tr/td/div/form/table[3]/tbody/tr[1]/td/a[2]')
                                    # 模拟鼠标移动到元素上并点击
                                    actions = ActionChains(driver)
                                    actions.move_to_element(element6).click().perform()
                                else:
                                    element5 = driver.find_element('xpath',
                                                                   '//*[@id="page-content"]/tbody/tr[1]/td[2]/table/tbody/tr/td/div/form/table[3]/tbody/tr[1]/td/a[3]')

                                    # 模拟鼠标移动到元素上并点击back to floors
                                    actions = ActionChains(driver)
                                    actions.move_to_element(element5).click().perform()

                            else:
                                print('Search Ended for This Block')
                                # 模拟点击back
                                element6 = driver.find_element('xpath',
                                                               '//*[@id="page-content"]/tbody/tr[1]/td[2]/table/tbody/tr/td/div/form/table[3]/tbody/tr[1]/td/a[2]')
                                # 模拟鼠标移动到元素上并点击
                                actions = ActionChains(driver)
                                actions.move_to_element(element6).click().perform()

# 构建DataFrame
data = {'PRN': A, 'STATUS': B}
df = pd.DataFrame(data)

print(df)
# df.to_csv('test_prn_status.csv', index=False)
print('done')

# 等待点击操作完成
time.sleep(3)

# 关闭浏览器
driver.quit()

