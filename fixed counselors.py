import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.parse import urlparse

api_key= 'a1fe3f09ee0f56aa05558e8efc6db52e'
def addr_to_lat_lon(addr):
    url = f'https://dapi.kakao.com/v2/local/search/address.json?query={addr}'
    url_headers = {"Authorization": "KakaoAK " + api_key}
    try:
        address_tude = json.loads(str(requests.get(url, headers=url_headers).text))
        tude = address_tude['documents'][0]['address']
        # 위도 경도만 가져오기.
        return [float(tude['x']), float(tude['y'])]
    except:
        return None



total_lst = []
for page in range(1, 17):
    sub_url = f'https://counselors.or.kr/KOR/user/find_center.php?ptype=&page={page}&sido=&searchkey='
    sub_resp = requests.get(sub_url)
    sub_soup = BeautifulSoup(sub_resp.text, 'html.parser')

    detail_tags = sub_soup.select("table[class=center_list] > tbody > tr > td:nth-child(6)")
    list_all = list()
    for href in detail_tags:
        result = href.find("a")["href"]
        result_except = result[1:]

        target_url_detail = f'https://counselors.or.kr/KOR/user{result_except}'
        resp = requests.get(target_url_detail)
        soup = BeautifulSoup(resp.content.decode('euc-kr', 'replace'), 'html.parser', from_encoding='euc-kr')
        detail_about = soup.find('table', {'class': 'center_info'})

        td_list = detail_about.find_all('td')

        # 각각의 정보를 list로 받기
        name_lst = td_list[0].get_text()
        address_lst = td_list[5].get_text()
        phone_lst = td_list[2].get_text()
        web_lst = td_list[4].get_text()

        temp = {}
        temp['공공/민간'] = '공공'
        temp['기관구분'] = '상담소'
        temp['기관명'] = name_lst
        temp['주소'] = address_lst
        temp['좌표']=addr_to_lat_lon(temp['주소'])
        temp['전화번호'] = phone_lst
        temp['홈페이지'] = web_lst
        total_lst.append(temp)

res = {}
res['정신건강관련기관_한국상담학회'] = total_lst
# json파일로 변환하기
res_json = json.dumps(res, ensure_ascii=False)
pprint(res_json)

#json파일로 저장하기
with open('전국_한국상담학회_상담소.json','w',encoding='utf-8') as f:
    f.write(res_json)