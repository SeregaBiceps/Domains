from selenium import webdriver
import time
import urllib.request, json
from datetime import datetime
 
names = ['Dildo', 'Jopa', 'Hate', 'Fake']

def get_info(name):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('http://tmsearch.uspto.gov/')
    print(driver.find_elements_by_tag_name('a'))
    link = driver.find_element_by_link_text('Basic Word Mark Search (New User)')
    link.click()
    radios = driver.find_elements_by_name('p_s_PARA1')
    radios[1].click()
    search = driver.find_element_by_name('p_s_PARA2')
    search.send_keys(name)
    submit = driver.find_elements_by_name('a_search')[1]
    submit.click()

    try:
        TSDRs = driver.find_elements_by_link_text('TSDR')
        TSDRs[0].click()
    except:
        driver.delete_all_cookies()
        driver.close()
        driver.quit()
        return(f'{name}\nThere\'s no such domain\n--------------------------')

    sleep = 0
    while True:
        sleep += 1
        if sleep >= 10:
            driver.delete_all_cookies()
            driver.close()
            driver.quit()
            return(f'{name}\nPage is loading too slow\n--------------------------')
        try:
            documents = driver.find_element_by_id('documentsTabBtn')
            documents.click()
            sleep = 0
            break
        except:
            time.sleep(1)

    cnt = 0
    while cnt < 3:
        try:
            TEAS = driver.find_element_by_partial_link_text('TEAS')
            break
        except:
            driver.find_element_by_id('statusTabBtn').click()
            documents.click()
            cnt += 1
        if cnt == 3:
            driver.delete_all_cookies()
            driver.close()
            driver.quit()
            return(f'{name}\nThere\'s no such document\n--------------------------')

    info = TEAS.get_attribute('href')
    driver.get(info)


    frame = driver.find_element_by_id('docPage')
    src = frame.get_attribute('src')
    driver.get(src)

    tds = driver.find_elements_by_tag_name('td')
    for i in tds:
        if('emailAddr' in i.get_attribute('headers')):
            domain = (i.text).split('@')[1]
            break

    driver.delete_all_cookies()
    driver.close()
    driver.quit()
    url = f'http://api.whois.vu/?q={domain}'

    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
        expire = datetime.fromtimestamp(data['expires'])
        return(f'{name}\n{domain}\n{expire}\n--------------------------')

for name in names:
    print(get_info(name))