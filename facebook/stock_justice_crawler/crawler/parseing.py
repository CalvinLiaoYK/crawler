import re
from datetime import datetime, timedelta


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


def get_company_content(company, browser):
    
    all_cont = browser.find_elements_by_css_selector("div[class='rq0escxv l9j0dhe7 du4w35lb']")
    
    for cont in all_cont:
        sens = cont.text.split('\n')
        for index, info in enumerate(sens):
            
            if re.search(r'的真實價值', info):
                sub_content = re.split(',|、|的真實價值', info)
                for i, sub in enumerate(sub_content):
                    code = re.search(r'\d{4}', sub)                        
                    if code:
                        code = code.group()
                        name = re.split(r'\(|（', sub)[0].strip()
                        name = re.sub(r'.\n', '', name)
                        company[name]['Code'] = code
                        
                        # get timestamp
                        for ts_index in range(5):
                            if re.search(r'分鐘|小時|昨天|[\d]{1,2}月[\d]{1,2}日', sens[index - (ts_index + 1)]):
                                ts = sens[index - (ts_index + 1)]

                        yyyymmdd, date = dateformatter(ts)                            
                        #company[name]['Timestamp'] = ts
                        company[name]['Date'] = yyyymmdd

            elif re.search(r'的 Ks =', info):
                index = re.split('的 Ks =', info)
                index_name = index[0].strip()
                index_value = index[1].strip()
                company[index_name]['Ks'] = index_value

            elif re.search(r'的 P / E =', info):
                index = re.split('的 P / E =', info)
                index_name = index[0].strip()
                index_value = index[1].split('=')[-1].strip()
                company[index_name]['P / E'] = index_value

            elif re.search(r'的 FRV =', info):
                index = re.split('的 FRV =', info)
                index_name = index[0].strip()
                index_value = index[1].split('=')[-1].strip()
                company[index_name]['FRV'] = index_value

            elif re.search(r'的 泡沫程度 =', info):
                index = re.split('的 泡沫程度 =', info)
                index_name = index[0].strip()
                index_value = index[1].split('=')[-1].strip()
                company[index_name]['泡沫程度'] = index_value
            
    return company
