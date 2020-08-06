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

def make_html_file(name, html):

    with open(name, 'w') as output_file:
        output_file.write(html)

name = 'Dildo'
fp_url = 'http://tmsearch.uspto.gov/'
info = get_key(fp_url)
key = info['key']

fp_html = make_request(fp_url)
make_html_file('first_page', fp_html)

sp_url = fp_url + info['searchss']
sp_html = make_request(sp_url)
make_html_file('second_page', sp_html)

tp_url = f'http://tmsearch.uspto.gov/bin/showfield?f=toc&state={key}&p_search=searchss&p_L=50&BackReference=&p_plural=yes&p_s_PARA1=live&p_tagrepl%7E%3A=PARA1%24LD&PARA2&p_s_PARA2={name}&p_tagrepl%7E%3A=PARA2%24COMB&p_op_ALL=AND&a_default=search&a_search=Submit+Query&a_search=Submit+Query'
tp_html = make_request(tp_url)
make_html_file('third_page', tp_html)