import requests
import time
import urllib.request, json
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def remove_files():
    dirs = os.listdir('.')
    for d in dirs:
        if '.' in d: continue
        direc = os.listdir(f'{d}')
        for i in direc:
            files = os.listdir(f'{d}/{i}/')
            for j in files:
                try: os.remove(f'{d}/{i}/{j}')
                except: continue

def make_request(url):
    print(f'Request to {url}...', end=" ")
    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    try:
        r = session.get(url, headers=headers, timeout=10)
    except:
        print('Connection lost!')
        return
    if '503 Service Unavailable' in r.text.encode('utf-8').decode('cp1251'): print('503 Error!')
    else: print('Ok!')
    return r.text.encode('utf-8').decode('cp1251')

def get_key(url):
    html = make_request(url)
    soup = BeautifulSoup(html, 'lxml')
    for i in soup.find_all('a'):
        if 'searchss' in i.get('href'):
            searchss = i.get('href')
            break
    key = searchss.split('state=')[1]
    info = {'searchss': searchss, 'key': key}
    return [info, html]

def make_html_file(src, html):
    folder = src.split('/')[0]
    subfolder = src.split('/')[1]
    if folder not in os.listdir():
        os.mkdir(folder)
    if subfolder not in os.listdir(folder):
        os.mkdir(f'{folder}/{subfolder}/')
    with open(f'{src}.html', 'w') as output_file:
        try:
            output_file.write(html)
        except:
            output_file.write('None')


def make_TSDRs(html, key):
    soup = BeautifulSoup(html, 'lxml')
    TSDRS = []
    hrefs = soup.find_all('a')
    for i in hrefs:
        if 'TSDR' in i.text:
            TSDRS.append(i.get('href'))
    while len(TSDRS) >= 50 and len(TSDRS) % 50 == 0:
        at = len(TSDRS) + 1 
        url2= f"http://tmsearch.uspto.gov/bin/showfield?f=toc&state={key[:-4]}.2.{at}"
        html2 = BeautifulSoup(make_request(url2), 'lxml')
        hrefs2 = html2.find_all('a')
        for j in hrefs2:
            if 'TSDR' in j.text:
                TSDRS.append(j.get('href'))
    return TSDRS

def make_TEASes(TSDRS):
    TEASES = []
    for i in TSDRS:
        number = (i.split('caseNumber=')[1]).split('&')[0]
        url = f'https://tsdr.uspto.gov/docsview/sn{number}'
        cnt = 0
        while True:
            if cnt == 10: make_html_file(f'html/TSDRS/TSDR_{number}', 'reached the limit of requests')
            try: html = make_request(url)
            except: make_html_file(f'html/TSDRS/TSDR_{number}', 'permission denied')
            if '503 Service Unavailable' not in html: break
            cnt += 1
        make_html_file(f'html/TSDRS/TSDR_{number}', html)

        soup = BeautifulSoup(html, 'lxml')
        for i in soup.find_all('a'):
            text = i.text
            acceptable = ['TEAS RF New Application', 'TEAS Plus New Application']
            if (text in acceptable):
                href = i.get('href')
                doc_id = href.split('docId=')[1]
                url = f'https://tsdrsec.uspto.gov/ts/cd/casedoc/sn{number}/{doc_id}/1/webcontent?scale=1'
                TEASES.append(url)
    return TEASES

def parse_TEASEs(TEASES):
    index = 0
    result = []
    for i in TEASES:
        domains = set()
        html = make_request(i)
        make_html_file(f'html/TEASES/TEAS_{index}', html)
        try: soup = BeautifulSoup(html, 'lxml')
        except: continue
        titles = ['SERIAL NUMBER']
        for i in soup.find_all('th', colspan='2'): titles.append(i.text)
        parsed = {}
        elems = {}
        cnt = 0
        for tr in soup.find_all('tr'):
            try:
                try:
                    title = tr.find('th', colspan='2').text.replace('\n', '').replace('\t', '').replace('*', '').strip()
                    if title in titles:
                        parsed[titles[cnt]] = elems
                        elems = {}
                        cnt += 1
                except: pass
                th = tr.find('th', headers='input').text.replace('\n', '').replace('\t', '').replace('*', '').strip()
                td = tr.find('td', headers='entered').text.replace('\n', '').replace('\t', '').replace('*', '').strip()
                if '@' in td and ';' in td:
                    for i in td.split(';'): 
                        domains.add(i.strip().split('@')[1])
                elif '@' in td: domains.add(td.strip().split('@')[1])
                elems[th] = td
            except: continue
        teas = parsed
        for domain in domains:
            parsed_domain = parse_domains(index, domain, teas)
            result.append(parsed_domain)
        index += 1
    return result

def make_json(url):
    print(f'Request to {url}...', end=" ")
    with urllib.request.urlopen(url, timeout=30) as url:
        data = json.loads(url.read().decode())
    print('Ok!')
    return data
    
def make_file(data, cnt, domain, teas):
    if 'py' not in os.listdir():
        os.mkdir('py')
    if 'parsed_domains' not in os.listdir('py'):
        os.mkdir('py/parsed_domains/')
    domain = domain.split('.')[0].replace('-', '_')
    with open(f'py/parsed_domains/{cnt}_{domain}.py', 'w') as dom_file:
        dom_file.write(f'_{domain} = {data}, {{\'TEAS\': {teas}}}')

def parse_domain(data, domain):
    whois_arr = data['whois'].split('\r\n')
    data['whois'] = {}
    for i in whois_arr:
        if '>>>' in i or 'NOTICE' in i or 'URL of the ICANN' in i or 'TERMS OF USE' in i or 'You agree that' in i: continue
        if ': ' not in i: continue
        key_value = i.split(': ')
        key = key_value[0].strip()
        value = key_value[1].strip()
        data['whois'][key] = value
    return data   

def parse_domains(cnt, domain, teas):
    dictionary = {}
    result = ''
    url = f'http://api.whois.vu/?q={domain}'
    try:
        data = make_json(url)
        data = parse_domain(data, domain)
        dictionary[domain] = data
        dictionary['teas'] = teas
        result = dictionary
        make_file(data, cnt, domain, teas)
    except:
        print(f'Request took more than 30 sec: {domain}')
    return result

def print_result(i, domain, teas):
    try: print(f"Domain: {i[domain]['domain']}")
    except: print('Domain: unknown')
    try: print(f"Expires: {datetime.fromtimestamp(i[domain]['expires'])}")
    except: print('Expires: unknown')
    try: print(f"Serial number: {i[teas]['SERIAL NUMBER']['SERIAL NUMBER']}")
    except: print('Serial number: unknown')
    try:
        if 'IMAGEOUT' not in i[teas]['MARK INFORMATION']['MARK']:
            print(f"Mark: {i[teas]['MARK INFORMATION']['MARK']}")
        else: print('Mark: unknown')
    except: print('Mark: unknown')
    print('---------------------------------')

session = requests.session()
name = 'knife'# input('insert word\n')
fp_url = 'http://tmsearch.uspto.gov/'
info = get_key(fp_url)
key = info[0]['key']

remove_files()

fp_html = info[1]
make_html_file('html/main_pages/first_page', fp_html)

sp_url = fp_url[:-1] + info[0]['searchss']
sp_html = make_request(sp_url)
make_html_file('html/main_pages/second_page', sp_html)

tp_url = f'http://tmsearch.uspto.gov/bin/showfield?f=toc&state={key}&p_search=searchss&p_L=50&BackReference=&p_plural=yes&p_s_PARA1=live&p_tagrepl%7E%3A=PARA1%24LD&PARA2&p_s_PARA2={name}&p_tagrepl%7E%3A=PARA2%24COMB&p_op_ALL=AND&a_default=search&a_search=Submit+Query&a_search=Submit+Query'
tp_html = make_request(tp_url)
make_html_file('html/main_pages/third_page', tp_html)

TSDRS = make_TSDRs(tp_html, key)
TEASES = make_TEASes(TSDRS)
result = parse_TEASEs(TEASES)

print('---------------------------------\n')
print(f"Found {len(result)} domains:")
print('\n---------------------------------')
free_domains = []
for i in result:
    try:
        domain, teas = i.keys()
        print_result(i, domain, teas)
        if (datetime.now() + timedelta(7) > datetime.fromtimestamp(i[domain]['expires'])):
            free_domains.append(i)
    except:
        continue

print(f"\nFound {len(free_domains)} free domains\n")
print('---------------------------------')
if len(free_domains) > 0:
    for i in free_domains:
        try:
            domain, teas = i.keys()
            print_result(i, domain, teas)
        except: continue