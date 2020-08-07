import requests
import time
import urllib.request, json
import os
from bs4 import BeautifulSoup

def remove_files():
    print('Removing old files...')
    dirs = os.listdir('.')
    for d in dirs:
        if '.' in d: continue
        direc = os.listdir(f'{d}')
        for i in direc:
            files = os.listdir(f'{d}/{i}/')
            for j in file
                try: os.remove(f'{d}/{i}/{j}')
                except: continue
    print('Old files has been removed!')

def make_request(url):
    print('Making a request...')
    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    r = session.get(url, headers=headers, timeout=5)
    print('Got some info!')
    return r.text.encode('utf-8').decode('cp1251')

def get_key(url):
    print('I\'m searching for token and next href...')
    main_html = make_request(url)
    hrefs = main_html.split('<A HREF="')
    for i in hrefs:
        if 'searchss' in i:
            last_index = i.find('"')
            searchss = i[:last_index]
    key = searchss.split('state=')[1]
    info = {'searchss': searchss, 'key': key}
    print('There they are!')
    return info

def make_html_file(src, html):
    print('Just trashing your folders...')
    folder = src.split('/')[0]
    subfolder = src.split('/')[1]
    if folder not in os.listdir():
        os.mkdir(folder)
    if subfolder not in os.listdir(folder):
        os.mkdir(f'{folder}/{subfolder}/')
    with open(f'{src}.html', 'w') as output_file:
        output_file.write(html)

def make_TSDRs(html):
    print('Making TSDRs...')
    soup = BeautifulSoup(html, 'lxml')
    TSDRS = []
    for i in soup.find_all('a'):
        if 'TSDR' in i.text:
            TSDRS.append(i.get('href'))
    print('Done!')
    return TSDRS

def make_TEASes(TSDRS):
    print('Making TEASes...')
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
            else:
                if cnt <= 3: print('Bullshit info, coming back...')
                else: print('GIVE ME THE FUCKING INFO!')
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
    print('Done with these requests!')
    return TEASES

def parse_TEASEs(TEASES):
    index = 0
    domains = []
    for i in TEASES:
        print('Parsing TEAS...')
        html = make_request(i)
        make_html_file(f'html/TEASES/TEAS_{index}', html)
        soup = BeautifulSoup(html, 'lxml')
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
                    for i in td.split(';'): domains.append(i.strip())
                elif '@' in td: domains.append(td)
                elems[th] = td
            except: continue
        if 'py' not in os.listdir():
            os.mkdir('py')
        if 'parsed_TSDRs' not in os.listdir('py'):
            os.mkdir('py/parsed_TSDRs/')
        with open(f'py/parsed_TSDRs/TSRD_{index}.py', 'w') as TSDR:
            TSDR.write(f'TSDR = {parsed}')
        index += 1
        print('I got one!')
    print('Phew... made it!')
    return domains

def parse_domains(domains):
    print('Now some serios stuff!')
    domain = set()
    for i in domains:
        domain.add(i.split('@')[1])
    domains = domain
    cnt = 0
    for domain in domains:
        print('Parsing domain...')
        url = f'http://api.whois.vu/?q={domain}'
        try:
            with urllib.request.urlopen(url) as url:
                data = json.loads(url.read().decode())

            whois_arr = data['whois'].split('\r\n')
            data['whois'] = {}
            for i in whois_arr:
                if '>>>' in i or 'NOTICE' in i or 'URL of the ICANN' in i or 'TERMS OF USE' in i or 'You agree that' in i: continue
                if ': ' not in i: continue
                key_value = i.split(': ')
                key = key_value[0]
                value = key_value[1]
                data['whois'][key] = value

            if 'py' not in os.listdir():
                os.mkdir('py')
            if 'parsed_domains' not in os.listdir('py'):
                os.mkdir('py/parsed_domains/')
            with open(f'py/parsed_domains/domain_{cnt}.py', 'w') as dom_file:
                domain = domain.split('.')[0]
                dom_file.write(f'_{domain}={data}')
            cnt += 1
        except: continue
        print('Parsed!')
    print('Finally all done!')

session = requests.session()
name = input('insert word\n')
fp_url = 'http://tmsearch.uspto.gov/'
info = get_key(fp_url)
key = info['key']

remove_files()

fp_html = make_request(fp_url)
make_html_file('html/main_pages/first_page', fp_html)

sp_url = fp_url + info['searchss']
sp_html = make_request(sp_url)
make_html_file('html/main_pages/second_page', sp_html)

tp_url = f'http://tmsearch.uspto.gov/bin/showfield?f=toc&state={key}&p_search=searchss&p_L=50&BackReference=&p_plural=yes&p_s_PARA1=live&p_tagrepl%7E%3A=PARA1%24LD&PARA2&p_s_PARA2={name}&p_tagrepl%7E%3A=PARA2%24COMB&p_op_ALL=AND&a_default=search&a_search=Submit+Query&a_search=Submit+Query'
tp_html = make_request(tp_url)
make_html_file('html/main_pages/third_page', tp_html)

TSDRS = make_TSDRs(tp_html)
TEASES = make_TEASes(TSDRS)
domains = parse_TEASEs(TEASES)
parse_domains(domains)