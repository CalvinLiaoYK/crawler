import re
import pandas as pd
import time
import logging
from logging_config import console_hdlr, file_hdlr
from parseing import get_company_content
from datetime import datetime, timedelta
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException

log_path = '../log'
exeday = datetime.now().strftime('%Y%m%d')

logger = logging.getLogger('fb_crawler')
logger.setLevel(logging.INFO)
logger.addHandler(console_hdlr())
logger.addHandler(file_hdlr(log_path, exeday))


def last_timestamp():
    
    date_class = ".b6zbclly.myohyog2.l9j0dhe7.aenfhxwr.l94mrbxd.ihxqhq3m.nc684nl6.t5a262vz.sdhka5h4"
    
    try:
        wait = WebDriverWait(browser, 1)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, date_class)))
        timestamp_list = browser.find_elements_by_css_selector(date_class)
    except(StaleElementReferenceException):
        print('stale element reference: element is not attached to the page document')
        
    timestamp = []
    
    for ts in timestamp_list:
        if ts.text != '':
            timestamp.append(ts.text)

    last_timestamp = timestamp[-1]
    
    return last_timestamp


def dateformatter(timestamp):

    if re.search(r'分鐘|小時|2020年12月19日', timestamp):
        mmdd = datetime.today().strftime('%m/%d')
    elif re.search(r'昨天', timestamp):
        mmdd = (datetime.today() - timedelta(1)).strftime('%m/%d')
    elif re.match(r'[\d]{1,2}月[\d]{1,2}日', timestamp):
        mmdd = re.sub(r'日', '', re.sub(r'月', '/', re.search(r'[\d]{1,2}月[\d]{1,2}日', timestamp).group()))
    else:
        print(f'error timestamp: {timestamp}')
        
    yyyymmdd = datetime.today().strftime('%Y/') + mmdd
    date = datetime.strptime(yyyymmdd, "%Y/%m/%d")

    return yyyymmdd, date


def date_of_post(start_date):
    
    last_height = browser.execute_script("return document.body.scrollHeight")
    time.sleep(2)
    
    # 最尾端時間戳記
    last_ts = last_timestamp()
    
    # 日期判斷
    yyyymmdd, date = dateformatter(last_ts)
    
    # 截止日判斷
    if date >= start_date:
        return True
    else:
        print(date)
        new_height = last_height + 1000
        browser.execute_script(f"window.scrollTo(0, {new_height});")
        last_ts = last_timestamp()
        
        if date > start_date:
            return True
        else:
            return False


def see_more():
    
    click_string = "div[class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p'][role='button']"

    try:
        wait = WebDriverWait(browser, 2)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, click_string)))
        read_button = browser.find_element_by_css_selector(click_string)
        browser.implicitly_wait(1)
        if read_button:
            browser.implicitly_wait(2)
            read_button.click()
    except ElementNotVisibleException:
        print("Exception：element not visible")
    except Exception as e:
        print(Exception, e) 


def to_file(company):
    
    df_list = []
    for com in company.keys():
        if len(company[com].keys()) == 6:
            company[com]['Name'] = com
            df_list.append(company[com])

    df = pd.DataFrame(df_list, columns=['Name', 'Code', 'Ks', 'P / E', 'FRV', '泡沫程度'])
    df.to_csv(f'../result/{exeday}.csv', index=False, encoding="utf-8-sig")


def main():

    # browser.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
    post = date_of_post()
    last_height = browser.execute_script("return document.body.scrollHeight")
    time.sleep(2)

    while(post):
        
        new_height = last_height + 500
        browser.execute_script(f"window.scrollTo(0, {new_height});")
        time.sleep(2)

        # 確認目前下拉範圍
        post = date_of_post()

    if not post:
        
        last_height = browser.execute_script("return document.body.scrollHeight")
        browser.execute_script(f"window.scrollTo(0, {last_height});")
        time.sleep(2)
        
        browser.execute_script("window.scrollTo(0, 0);")
        logger.info("check start")

        check_height = 0
        while(check_height < last_height):
            browser.execute_script(f"window.scrollTo(0, {check_height});")
            logger.info("scroll down 500")

            time.sleep(2)
            see_more()
            logger.info("click see_more")
            
            get_company_content(company, browser)
            check_height += 500

    to_file(company)
    logger.info("Save file")

    browser.close()
    logger.info("Close browser")
    logger.info("===================Finish===================")


if __name__ == '__main__':
    logger.info("===================Start===================")
    browser = webdriver.Chrome(executable_path='..\\webdriver\\chromedriver.exe')
    browser.get('https://www.facebook.com/groups/1189431674567215/')
    logger.info("Open browser")
    company = defaultdict(dict)
    time.sleep(5)
    
    start_date = datetime.today()
    main(start_date)
