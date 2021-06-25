import time

from selenium import webdriver

driver = webdriver.Chrome('/Users/doongle/Downloads/chromedriver')
url_start = 'https://news.naver.com'
keywords= ['닌텐도스위치','PS5','XBOX']


def finput_keyword(keyword):
    driver.switch_to.window(driver.window_handles[0])
    driver.get(url_start)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//input[@class="text_index"]').send_keys(keyword)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//button[@type="submit"]').click()
    driver.implicitly_wait(10)
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    driver.implicitly_wait(10)
    time.sleep(1)
    driver.find_elements_by_xpath('//a[@role="option"]')[1].click()
    driver.implicitly_wait(10)
    time.sleep(1)
    return driver


def fmake_file(keyword):
    file_name = 'naver_news_' + keyword + "_" + time.strftime('%y%m%d_%H%M%S')+".txt"
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('{}\t{}\t{}\t{}\n'.format('페이지','키워드','제목','URL'))
    return file_name


def fwrite_news(i, keyword, news_title_clean, news_url, file_name):
    t_list = [i, keyword, news_title_clean, news_url]
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write('{}\t{}\t{}\t{}\n'.format(*t_list))
    return


def crawl_news_selenium(driver, keyword, i, file_name):
    bodies = driver.find_elements_by_xpath('//ul[@class="list_news"]/li')
    for body in bodies:
        news_title_elm = body.find_elements_by_xpath('.//a[@class="news_tit"]')[0]
        news_title = news_title_elm.get_attribute('title')
        try:
            news_url_elm = body.find_elements_by_xpath('.//a[@class="info"]')[0]
            news_url = news_url_elm.get_attribute('href')
        except:
            news_url = ''

        news_title_clean = news_title.replace('\n', '').replace('\t','').replace('\r', '').strip()
        fwrite_news(i, keyword, news_title_clean, news_url, file_name)

    page_nav = driver.find_element_by_xpath('//div[@class="sc_page_inner"]')
    next_page = page_nav.find_element_by_link_text(str(int(i)+1))
    next_page.click()
    driver.implicitly_wait(10)
    time.sleep(1)
    return

def fmain():
    for keyword in keywords:
        output_file_name = fmake_file(keyword)
        driver = finput_keyword(keyword)
        for i in range(1, 2):
            print(i)
            crawl_news_selenium(driver, keyword, i, output_file_name)
            time.sleep(1)
        driver.close()

fmain()