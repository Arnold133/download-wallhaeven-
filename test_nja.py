import unittest
import requests
import pymysql
import uuid
import time
import random
from bs4 import BeautifulSoup
from time import sleep
import wikipedia
import redis

class test_wiki(unittest.TestCase):

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

    current_count = 0

    def test_cmano(self):

        # 开始运行时间
        start = time.time()

        for i in range(1, 2):

            print("正在抓取第：" + str(i) + "页内容")

            # url = 'https://njav.tv/zh/tags/fc2?sort=most_favourited?page=' + str(i)
            # url = 'https://njav.tv/zh/series/cc288a42d6bc324d?page=' + str(i)
            url = 'https://njav.tv/zh/actresses/94d4610a1a214647?sort=most_favourited?page=' + str(i)
            url_cili_sou = 'https://cili.lat/search?q='
            url_cili_zhongzi = 'https://cili.lat'
            base_url = 'https://njav.tv/zh/'

            ua = random.choice(self.user_agent_list)

            headers = {'Accept': '*/*',
                       'Host': 'njav.tv',
                       'User-Agent': ua}

            respose = requests.get(url, headers=headers)

            # status_code 为返回的状态码
            # text为返回的数据
            # print(respose.text)
            # 将text转换成json格式
            soup = BeautifulSoup(respose.text, 'lxml')

            count = 0

            # 获取列表
            divs = soup.select('.detail>a')

            for div in divs:

                fanhao = div.get('href').replace('v/', '')
                name = div.get_text()
                print(fanhao)

                id = str(uuid.uuid1())
                create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                type = 'Hiyori Kojima'
                url2 = url_cili_sou + fanhao
                result = ''

                if count < self.current_count:
                    continue

                time.sleep(6)

                ua2 = random.choice(self.user_agent_list)

                headers2 = {'Accept': '*/*',
                            'Host': 'cili.lat',
                            'User-Agent': ua2}

                res2 = requests.get(url2, headers=headers2)

                if res2.status_code != 200:
                    print('发生错误！正在重试！')

                soup2 = BeautifulSoup(res2.text, 'lxml')

                files = soup2.select('.file-list')

                if len(files) > 0:

                    for file in files:
                        list = file.find('a')
                        if list:
                            href = list.get('href')
                            namesss = list.text

                            if fanhao.lower() in namesss.lower():

                                url3 = url_cili_zhongzi + href

                                res3 = requests.get(url3, headers=headers2)

                                if res3.status_code != 200:
                                    print('发生错误！正在重试！')

                                soup3 = BeautifulSoup(res3.text, 'lxml')

                                magnet = soup3.select('#input-magnet')
                                if magnet:
                                    for m in magnet:
                                        cili = m.get('value')
                                        result = cili.split("&")[0]
                                        print(result)

                                tuple = (id, type, name, fanhao, result, create_time)

                                conn = pymysql.connect(
                                    # host='huan.yufei.cloudns.ch',
                                    # port=60006,
                                    # user='root',
                                    # password='hk_mm9966',
                                    host='localhost',
                                    port=3306,
                                    user='root',
                                    password='root',
                                    database='test',
                                    charset='utf8mb4',
                                    autocommit=True  # 自动提交
                                )

                                # 获取一个光标
                                cursor = conn.cursor()
                                # 定义要执行的sql语句
                                sql = 'insert into njav(id, type, name, fanhao, cili, create_time)' \
                                      'values(%s,%s,%s,%s,%s,%s)'
                                # 执行传入的sql语句(多条数据插入和一条数据插入调用方法不同)
                                cursor.execute(sql, tuple)
                                cursor.close()
                                conn.close()


if __name__ == "_main_":
    unittest.main()
