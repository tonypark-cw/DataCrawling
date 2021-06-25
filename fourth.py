import requests
import xml.etree.ElementTree as ET
import time

headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/86.0.4240.272 Whale/2.9.118.16 Safari/537.36'}
servicekey ='UwenAwvEyeeCzH4z4%2FUSDP%2BFyYjtgLUxlnSGt74ofVi21OU2iOh%2FI28cUt0iTy5hd3br%2BE%2BtTHWhrY2CXIJb7Q%3D%3D'

d_code = '11440'



def fetch_deals(deal_date):
    url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade'
    queryParams = '?' + 'ServiceKey=' + servicekey + '&LAWD_CD='+d_code+ '&DEAL_YMD='+deal_date
    res = requests.get(url + queryParams, headers=headers)
    root = ET.fromstring(res.content)
    today = time.strftime('%y%m%d_%H%M%S')

    with open('./r_code.csv', 'r') as f:
        datas = f.readlines()
        dict_g = {}
        for data in datas:
            q = data.split('\t')
            q[1] = q[1].replace('\n', '')
            dict_g[q[1]] = q[0]
    elements = root.iter(tag='item')
    for element in elements:
        price = element.find('거래금액').text
        const_year = element.find('건축년도').text
        year = element.find('년').text
        month = element.find('월').text
        day = element.find('일').text
        dong = element.find('법정동').text
        apt = element.find('아파트').text
        square = element.find('전용면적').text
        floor = element.find('층').text
        elm_list =[today, dict_g.get(d_code), price, const_year, year, month, day, dong, apt, square, floor]
        try:
            f = open(deal_date + '_' + dict_g.get(d_code) + '_' + deal_date, 'r')
        except:
            f = open(deal_date+'_'+dict_g.get(d_code)+'_'+deal_date, 'w')
            f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format('조사일','거래구역','거래금액','건축년도','년','월','일','법정동','아파트','전용면적','층'))
        finally:
            f.close()
        with open(deal_date+'_'+dict_g.get(d_code)+'_'+deal_date, 'a') as f:
            f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(*elm_list))


deal_date = time.strftime('%Y%m')
# while True:
print(deal_date)
fetch_deals(deal_date)
