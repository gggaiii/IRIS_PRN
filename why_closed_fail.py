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

# 打开网页
# url = "https://www1.iris.gov.hk/eservices"
url = 'https://www1.iris.gov.hk/eservices'
driver.get(url)

# 找到要点击的元素并模拟点击
# button = driver.find_element_by_xpath('//button[@id="your-button-id"]')  # 使用 XPath 定位元素
# button = driver.find_element_by_xpath('//*[@id="menu1_2"]')  # 使用 XPath 定位元素
# button = driver.find_element('id', 'menu1_2')  # 使用 find_element 方法
# button.click()

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

# 测试是否完成验证码操作
# element2 = driver.find_element('xpath', '//*[@id="page-content"]/tbody/tr[1]/td[2]/table/tbody/tr/td/div[1]/form/div/label[1]')
# 模拟鼠标移动到元素上并点击
# actions = ActionChains(driver)
# actions.move_to_element(element2).click().perform()

# 定位输入框
input_element = driver.find_element('xpath', '//*[@id="SDevelopmentNameEng"]')
# 输入字符串
input_element.send_keys("WINNER BUILDING")

time.sleep(1.5)
# 在网站空白处模拟一次点击,以关闭下拉栏，暴露continue按钮
elementempty = driver.find_element('xpath', '//*[@id="zoomIn"]/i')
# 模拟鼠标移动到元素上并点击
actions = ActionChains(driver)
actions.move_to_element(elementempty).click().perform()

time.sleep(1.5)

# 模拟点击continue
element3 = driver.find_element('xpath', '//*[@id="continueButton"]')
# 模拟鼠标移动到元素上并点击
actions = ActionChains(driver)
actions.move_to_element(element3).click().perform()

# 模拟点击表格第一行
element4 = driver.find_element('xpath', '//*[@id="multiSelect"]/tr[2]/td[2]')
# //*[@id="multiSelect"]/tr[7]/td[1]
# //*[@id="multiSelect2"]/tr[33]/td[1]
# 模拟鼠标移动到元素上并点击
actions = ActionChains(driver)
actions.move_to_element(element4).click().perform()

# 模拟点击表格“--”格，显示全部unit
element5 = driver.find_element('xpath', '//*[@id="multiSelect"]/tr[2]/td[1]')
# 模拟鼠标移动到元素上并点击
actions = ActionChains(driver)
actions.move_to_element(element5).click().perform()

# 获取网站的HTML内容
html = driver.page_source

# 使用 BeautifulSoup 解析页面源码
soup = BeautifulSoup(html, 'html.parser')
tbody = soup.find_all('tbody')[1]

# 提取数据
records = []
status = []
for row in tbody.select('tr'):
    link = row.find('a')
    if link:
        PRN = link.text.strip().replace('(', '').replace(')', '')  # 去除括号和空格  # 提取 <a> 元素的文本内容并去除首尾空格
        records.append(PRN)

    link1 = row.find('span')
    if link1:
        STA = link1.text.strip().replace('(', '').replace(')', '')  # 去除括号和空格  # 提取 <a> 元素的文本内容并去除首尾空格
        status.append(STA)

# 网站下方按钮也被纳入table，手动删除
records = records[:-2]
status = status[:-1]

# 构建DataFrame
data = {'PRN': records, 'STATUS': status}
df = pd.DataFrame(data)
# 去掉前两行，网站上方按钮，手动删除
df = df[2:]

print(df)
# df.to_csv('test_prn_status.csv', index=False)
print('done')

# 等待点击操作完成
time.sleep(3)

# 关闭浏览器
driver.quit()