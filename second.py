import requests as req
from lxml import html
import time
from tkinter import Tk, filedialog


def crawl_news(keyword='닌텐도 스위치'):
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/86.0.4240.272 Whale/2.9.118.16 Safari/537.36'}
    row = []
    i = 1
    while True:
        page_number = str(i)
        url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=' + keyword + '&sort=1&photo=0&field=0\
        &pd=3&ds=2020.12.01&de=2021.05.31&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:\
        from20210101to20210531,a:all&start=' + page_number
        res = req.get(url, headers=headers)

        trees = html.fromstring(res.content)
        bodies = trees.xpath('//ul[@class="list_news"]/li')
        for body in bodies:
            news_title = body.xpath('.//a[@class="news_tit"]/@title')[0]
            try:
                news_url = body.xpath('.//a[@class="info"]/@href')[0]
            except:
                news_url = ''
            result = news_title.replace('\n', '').replace('\t', '').replace('\r', '').strip()
            results = dict()
            if news_url:
                results['페이지'] = (i//10) + 1
                results['키워드'] = keyword
                results['제목'] = result
                results['URL'] = news_url
                row.append(results)
        if i >= 32:
            break
        i = i + 10
        time.sleep(3)
    return row


def save_file(datas, file_name):
    with open(file_name, 'a') as f:
        f.write('{}\t{}\t{}\t{}\n'.format('페이지', '키워드','제목','URL'))
        for data in datas:
            f.write('{}\t{}\t{}\t{}\n'.format(data['페이지'], data['키워드'],data['제목'],data['URL']))


def naming(keyword):
    file_name = '{}_{}'.format(time.strftime('%y%m%d_%H%M%S'), keyword)
    return file_name


def main():
    keywords = ['GPT-3', '인공지능', '텐서플로', '네이버', '카카오','라인','쿠팡','배달의민족']
    for keyword in keywords:
        save_file(crawl_news(keyword), naming(keyword))


def open_file():
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir='./', title='Open Data Files', filetypes=(('data files', "\
    *.csv;*.xls"), ('all files', '*.*')))
    with open(root.filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line, end='')

# open_file()

main()

