import requests as req
import bs4
import selenium
from lxml import html

#네이버 뉴스
# url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=105'

#쿠팡
# url = 'https://www.coupang.com/np/search?rocketAll=true&q=%EB%8B%8C%ED%85%90%EB%8F%84%EC%8A%A4%EC%9C%84%EC%B9%98'

#국민청원
# url = 'https://www1.president.go.kr/petitions'

#지식인
# url = 'https://kin.naver.com/'

#팍스넷
url = 'https://www.paxnet.co.kr/'


headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.272 Whale/2.9.118.16 Safari/537.36'}
res = req.get(url, headers=headers)

tree = html.fromstring(res.content)

#네이버 뉴스 조건
# titles = tree.xpath('//div[@class="cluster_text"]/a/text()')
# links = tree.xpath('//div[@class="cluster_text"]/a')

#쿠팡 닌텐도스위치 조건
# titles = tree.xpath('//dl[@class="search-product-wrap"]//div[@class="name"]/text()')

#국민 청원
# titles = tree.xpath('//div[@class="bl_wrap"]//a/text()')

#네이버 지식인
# titles = tree.xpath('//div[@class="ranking_section"]//a[@class="ranking_title"]/text()')

#팍스넷
titles = tree.xpath('//div[@class="tab-body"]/ol/li/a/span/text()')

# print(titles)
results = []

for title in titles:
    title_clean = title.replace('\n', '').replace('\t', '').replace('\r', '').strip()
    results.append(title_clean)

for i in range(len(results)):
    print(results[i])
    # print( links[i].attrib['href'])
