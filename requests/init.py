import requests
import time
# import logging
# try:
#     import http.client as http_client
# except ImportError:
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

session = requests.session()

def make_request(url):

    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    r = session.get(url, headers=headers, timeout=5)
    return r.text.encode('utf-8').decode('cp1251')

def get_key(url):

    main_html = make_request(url)
    hrefs = main_html.split('<A HREF="')
    for i in hrefs:
        if 'searchss' in i:
            last_index = i.find('"')
            searchss = i[:last_index]
    key = searchss.split('state=')[1]
    info = {'searchss': searchss, 'key': key}
    return info

def make_html_file(src, html):

    with open(f'requests/{src}.html', 'w') as output_file:
        output_file.write(html)

name = 'Dildo'
fp_url = 'http://tmsearch.uspto.gov/'
info = get_key(fp_url)
key = info['key']

fp_html = make_request(fp_url)
make_html_file('main_pages/first_page', fp_html)

sp_url = fp_url + info['searchss']
sp_html = make_request(sp_url)
make_html_file('main_pages/second_page', sp_html)

tp_url = f'http://tmsearch.uspto.gov/bin/showfield?f=toc&state={key}&p_search=searchss&p_L=50&BackReference=&p_plural=yes&p_s_PARA1=live&p_tagrepl%7E%3A=PARA1%24LD&PARA2&p_s_PARA2={name}&p_tagrepl%7E%3A=PARA2%24COMB&p_op_ALL=AND&a_default=search&a_search=Submit+Query&a_search=Submit+Query'
tp_html = make_request(tp_url)
make_html_file('main_pages/third_page', tp_html)

hrefs = tp_html.split('<A HREF="')
TSDRS = []
for i in hrefs:
    if 'TSDR' in i:
        last_index = i.find('"')
        TSDRS.append(i[:last_index])

TEASES = []
for i in TSDRS:
    number = (i.split('caseNumber=')[1]).split('&')[0]
    url = f'https://tsdr.uspto.gov/docsview/sn{number}'
    html = make_request(url)
    make_html_file(f'TSDRS/TSDR_{number}', html)
    hrefs = html.split('<a href="')
    for i in hrefs:
        RF_index = i.find('TEAS RF New Application')
        Plus_index = i.find('TEAS Plus New Application')
        if (RF_index != -1 or Plus_index != -1):
            last_index = i.find('"')
            href = i[:last_index]
            doc_id = href.split('docId=')[1]
            url = f'https://tsdrsec.uspto.gov/ts/cd/casedoc/sn{number}/{doc_id}/1/webcontent?scale=1'
            TEASES.append(url)

index = 0
for i in TEASES:
    html = make_request(i)
    make_html_file(f'TEASES/TEAS_{index}', html)
    index += 1
    table = html.split('<tr bgcolor="')[1]
    trs = table.replace('\t', '').replace('\n', '').split('<tr')
    make_html_file(f'info/info_{index}', table)
    for i in trs:
        try:
            th = i.split('<td')[0]
            td = i.split('<td')[1]
            last_index = th.find('</')
            th = th[:last_index]
            last_index = td.find('</')
            td = td[:last_index]
            th_res = ''
            td_res = ''
            for i in range(len(th)):
                if th[-i-1] == '>': break
                th_res += th[-i-1]
            th = ''
            for i in range(len(th_res)):
                if i > 0:
                    if th_res[-i] == " " and th_res[-i-1] == " ": continue
                th += th_res[-i-1]

            for i in range(len(td)):
                if td[-i-1] == '>': break
                td_res += td[-i-1]
            td = ''
            for i in range(len(td_res)):
                if i > 0:
                    if td_res[-i] == " " and td_res[-i-1] == " ": continue
                td += td_res[-i-1]
            print(th+'\n'+td+'\n----------------')
        except: continue
    # print(trs)