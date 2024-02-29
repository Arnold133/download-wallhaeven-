import requests
import os
import time
import threading
from time import sleep


class Wallhaven_master(threading.Thread):


    def __init__(self):
        super(Wallhaven_master, self).__init__()
        self.url_user = 'https://wallhaven.cc/api/v1/collections?apikey=key'  # 用的时候需要填写自己的api key
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        }
        self.names = []
        self.colle_id = []
        self.pic_id = {}
        self.DLed = []
        self.DLread = []
        self.DLtmp = []

    def get_data(self, a):
        r = requests.get(a, headers=self.headers)
        req = r.json()
        data = req['data']
        return data

    def get_pic_id(self):

        data = self.get_data(self.url_user)
        for x in data:
            colle = x['id']
            self.colle_id.append(colle)

        # 开始运行时间
        start = time.time()
        for x in self.colle_id:
            is_done = 0
            if not os.path.exists('WH-pics'):
                os.mkdir("WH-pics")
            os.chdir('WH-pics')
            for xi in self.colle_id:
                if not os.path.exists(str(xi)):
                    os.mkdir(str(xi))
            
            # 计算重复次数，超过五次停止
            count_have = 0

            # 获取总共的页数
            url = f"https://wallhaven.cc/api/v1/collections/username/{x}?apikey=key"
            r = requests.get(url, headers=self.headers)
            req = r.json()
            data = req['data']
            total_page = req['meta'].get('last_page')

            for i in range(1, total_page + 1):

                if is_done == 1:
                    continue

                sleep(3.5)
                url = f"https://wallhaven.cc/api/v1/collections/username/{x}?apikey=key={i}"
                data = self.get_data(url)
                self.pic_id[x] = []
                for y in data:
                    path = y['path']

                    if is_done == 1:
                        continue

                    dirname, basename = os.path.split(path)

                    img_path = f"/download/pics/{x}/{basename}"

                    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                    print("运行时间:%.2f秒" % (time.time() - start))
                    print(f"正在下载收藏夹{x}的第{i}页的 ：{basename}")

                    if not os.path.exists(img_path):
                        r = requests.get(path, stream=True)
                        with open(img_path, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=32):
                                f.write(chunk)
                        sleep(3.5)
                    else:
                        print("这个已经有了，跳过")
                        count_have += 1
                        if count_have > 5:
                        	is_done = 1
                        	print("检测到五个重复，自动完成")
                    # self.pic_id[x].append(path)

    def start(self):
        self.get_pic_id()

if __name__ == "__main__":
    Wallhaven_master().start()
