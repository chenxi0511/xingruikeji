import time
import pandas as pd
from selenium import webdriver

options = webdriver.ChromeOptions()

# 设置请求头信息
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36')

# 禁用 Chrome 的自动化控制特性和自动化扩展程序
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

browser = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
url = 'https://iftp.chinamoney.com.cn/english/bdInfo/'

try:
    # 手动操作一遍
    browser.get(url)
    time.sleep(5)

    # 选择国债筛选条件
    # bond_type_select = browser.find_element_by_xpath('//*[@id="resetValue"]/div/div[4]/div[1]/label')
    # bond_type_options = bond_type_select.find_elements_by_tag_name('option')
    # for option in bond_type_options:
    #     if option.text == 'Treasury Bond':
    #         option.click()
    #         break
    bond_type_select = browser.find_element_by_xpath('//*[@id="resetValue"]/div/div[4]/div[1]/label')
    bond_type_select.click()
    option = bond_type_select.find_element_by_xpath('//*[@id="Bond_Type_select"]/option[2]')
    option.click()

    issue_year_select = browser.find_element_by_xpath('//*[@id="resetValue"]/div/div[6]/div[1]/label')
    issue_year_options = issue_year_select.find_elements_by_tag_name('option')
    for option in issue_year_options:
        if option.text == '2023':
            option.click()
            break

    search_btn = browser.find_element_by_xpath('//*[@id="resetValue"]/div/div[8]/a[1]')
    search_btn.click()
    time.sleep(5)

    # 解析网页内容
    df_list = []
    while True:
        # page_source = browser.page_source
        # df = pd.read_html(page_source)[0].dropna()
        # df_list.append(df)
        page_source = browser.page_source
        df = pd.read_html(page_source, header=0)[0]
        df_list.append(df)

        # # 循环等待，直到所有 ISIN 数据都加载出来
        # while len(df_list[-1]['ISIN'].unique()) < len(df_list[-1]):
        #     time.sleep(1)
        #     page_source = browser.page_source
        #     df_list[-1] = pd.read_html(page_source, header=0)[0]


        next_page_btn = browser.find_elements_by_xpath('//a[@id="nextPage"]')
        if len(next_page_btn) == 0:
            break

        next_page_btn[0].click()
        time.sleep(5)

    df = pd.concat(df_list, ignore_index=True)
    df.columns = ['ISIN', 'Bond Code', 'Issuer', 'Bond Type',  'Issue Date', 'Latest Rating']

    # 保存为 CSV 文件
    df.to_csv('treasury_bond_2023.csv', index=False)
    print(df)
except Exception as e:
    print(e)
finally:
    browser.quit()
