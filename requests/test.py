import requests

session = requests.session()
print(session)

headers = {
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
r = session.get('http://tmsearch.uspto.gov/', headers=headers, timeout=5)
print(requests.utils.dict_from_cookiejar(session.cookies))
