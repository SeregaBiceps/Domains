import requests
import time

session = requests.session()
def make_request(url):
    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    r = session.get(url, headers=headers, timeout=5)
    return r.text.encode('utf-8').decode('cp1251')

def get_key():
    url = 'http://tmsearch.uspto.gov/'
    main_html = make_request(url)
    hrefs = main_html.split('<A HREF="')
    for i in hrefs:
        if 'searchss' in i:
            last_index = i.find('"')
            searchss = i[:last_index]
    key = searchss.split('state=')[1]
    info = {'searchss': searchss, 'key': key}
    return info

name = 'Dildo'

info = get_key()

with open('first_page.html', 'w') as output_file:
    output_file.write(make_request('http://tmsearch.uspto.gov/'))

waste_time = make_request('http://tmsearch.uspto.gov/'+info['searchss'])

with open('second_page.html', 'w') as output_file:
    output_file.write(waste_time)

print(info['key'])

search_html = f"http://tmsearch.uspto.gov/bin/showfield?f=toc&state={info['key']}&p_search=searchss&p_L=50&BackReference=&p_plural=yes&p_s_PARA1=live&p_tagrepl%7E%3A=PARA1%24LD&expr=PARA1+AND+PARA2&p_s_PARA2={name}&p_tagrepl%7E%3A=PARA2%24COMB&p_op_ALL=AND&a_default=search&a_search=Submit+Query&a_search=Submit+Query"

mark_html = make_request(search_html)


# 4810:53y70w.1.1
# http://tmsearch.uspto.gov/bin/gate.exe?f=searchss&state=4802:emdpd6.1.1
# http://tmsearch.uspto.gov/bin/showfield?f=toc&state=4805:nhlk7k.1.1&p_search=searchss&p_L=50&BackReference=&p_plural=yes&p_s_PARA1=live&p_tagrepl%7E%3A=PARA1%24LD&expr=PARA1+AND+PARA2&p_s_PARA2=Dildo&p_tagrepl%7E%3A=PARA2%24COMB&p_op_ALL=AND&a_default=search&a_search=Submit+Query&a_search=Submit+Query
# http://tmsearch.uspto.gov/bin/showfield?f=toc&state=4802%3Aemdpd6.1.1&p_search=searchss&p_L=50&BackReference=&p_plural=yes&p_s_PARA1=live&p_tagrepl%7E%3A=PARA1%24LD&expr=PARA1+AND+PARA2&p_s_PARA2=Dildos&p_tagrepl%7E%3A=PARA2%24COMB&p_op_ALL=AND&a_default=search&a_search=Submit+Query&a_search=Submit+Query

with open('third_page.html', 'w') as output_file:
    output_file.write(mark_html)