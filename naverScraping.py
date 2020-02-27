import os
import sys
import urllib.request
import urllib
import requests
from bs4 import BeautifulSoup
import json
import re

# 오픈 API 아이디, 비번 (최초 설정 후 건드리지 말 것)
client_id = "6WYnMfrdnoyoYlultDEa"
client_secret = "2v07I3vRdY"

# keyword_1 : 첫번째 키워드
# keyword_2 : 두번째 키워드
# keyword_3 : 세번째 키워드
# 첫번째 키워드 + 두번째 키워드로 검색이 진행됩니다.
# 예를 들어, 첫번째 키워드가 ['개', '고양이', '토끼'] 이고
# 두번째 키워드가 ['1', '2'] 이면,
# 개 1, 개 2, 고양이 1, 고양이 2, 토끼 1, 토끼 2 처럼
# 키워드 1 개수 * 키워드 2 개수 만큼 검색 쿼리가 생성됩니다.
# 세번째 키워드는, 추가적으로 단일 키워드를 검색하고 싶은 경우 활용합니다.

#keyword_1 = ['강아지', '고양이']
#keyword_2 = ['토끼', '공원']

display = 30  # 각 키워드 당 검색해서 저장할 기사 수


#
#
# 여기서부터는 코드입니다 (신경 안쓰셔도 됩니다!)
#
#
#

# Input(str) : 뉴스에 검색할 단어 넣기
def news_search(min_name):
    encText = urllib.parse.quote(min_name)
    url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + "&display=" + str(display) + "&sort=sim"
    # json 결과
    # url = "https://openapi.naver.com/v1/search/news.xml?query=" + encText # xml 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        # response_body_str = response.read().decode('utf-8')
        response_body_str = response.read().decode('utf-8')
        json_acceptable_string = response_body_str.replace("'", "\"")
        response_body = json.loads(response_body_str)
        title_link = {}
        for i in range(0, len(response_body['items'])):
            title_link[response_body['items'][i]['title']] = response_body['items'][i]['link']

        return title_link

    else:
        print("Error Code:" + rescode)


# extract urls from correspoding response_body
def get_url(resbody):
    title_link = {}
    # print(str(len(resbody['items'])) + ' length of resbody of items')
    for i in range(0, len(resbody['items'])):
        # print(resbody['items'][i]['title'])
        title_link[resbody['items'][i]['title']] = resbody['items'][i]['link']
    return title_link


# using url list, crawl html and store them as .html
def url_to_html(title_links, cur_keyword1):
    # using url, store them into .html
    # 1. Make a single html file and add links to it
    filename = re.sub("[/:*?\"<>|]", "", cur_keyword1)
    f = open(filename + '.html', 'w', encoding='UTF-8')
    for k in title_links.keys():
        ''' # 2. Make seperate folder for each keyword combiantion 
        filename = re.sub("[/:*?\"<>|]", "", k) 
        path = os.path.abspath(".\\" + cur_keyword1) 
        f = open(os.path.join(path, filename) +'.html', 'w', encoding='UTF-8') 
        '''
        f.write("<A href=" + title_links[k] + ">" + k + "</A>" + "<br></br>")

        # 키워드 1 + 키워드 2 조합으로 검색


def keyword_combined(keyword_1, keyword_2):
    for i in range(len(keyword_1)):
        ''' # Make folders for each articles # Uncomment it when you use "2" 
        in url_to_html function if not os.path.exists(keyword_1[i]): os.makedirs(keyword_1[i])
         '''
        title_links = {}
        if len(keyword_2) == 0:
            title_links = {**title_links, **(news_search(keyword_1[i]))}
        else:
            for j in range(len(keyword_2)):
                title_links = {**title_links, **(news_search(keyword_1[i] + " " + keyword_2[j]))}
        url_to_html(title_links, keyword_1[i])


if __name__ == '__main__':
    keyword_combined('대웅', '제약')
