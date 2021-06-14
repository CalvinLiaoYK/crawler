import re


def get_company_content(company, browser):
    
    titles = browser.find_elements_by_css_selector("div[class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q']")
    values = browser.find_elements_by_css_selector("div[class='o9v6fnle cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q']")
    # timestamps = browser.find_elements_by_css_selector(".b6zbclly.myohyog2.l9j0dhe7.aenfhxwr.l94mrbxd.ihxqhq3m.nc684nl6.t5a262vz.sdhka5h4")
    
    # title
    for title in titles:
        if title.text != '':
            content = title.text
            
            if re.search(r'的真實價值', content):
                sub_content = re.split(',|、|的真實價值', content)
                for i, sub in enumerate(sub_content):

                    code = re.search(r'\d{4}', sub)                        
                    if code:
                        code = code.group()
                        name = re.split(r'\(|（', sub)[0].strip()
                        name = re.sub(r'.\n', '', name)
                        company[name]['Code'] = code
                        
    # value            
    for value in values:
        if value.text != '':
            infos = value.text.split('\n')

            for i, info in enumerate(infos):

                if re.search(r'的真實價值', info):
                    code = re.search(r'\d{4}', info)
                    if code:
                        code = code.group()
                        name = re.split(r'\(|（', info)[0].strip()
                        name = re.sub(r'.\n', '', name)
                        company[name]['Code'] = code

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
