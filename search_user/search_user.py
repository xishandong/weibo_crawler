import re
import time
from urllib.parse import parse_qs, urlparse
from concurrent.futures import ThreadPoolExecutor
from search_key.search_key import searchKey
from download.download import source_downloader


class user(searchKey):
    def __init__(self, id):
        super().__init__()
        self.cookies = {
            '__bid_n': 填你的cookie,
            'FPTOKEN': 填你的cookie,
            'WEIBOCN_FROM': 填你的cookie,
            'SUB': 填你的cookie,
            '_T_WM': 填你的cookie,
            'MLOGIN': '1',
        }
        self.id = id
        self.urls = 'https://m.weibo.cn/api/container/getSecond'
        response = self.session.get('https://m.weibo.cn/api/config', cookies=self.cookies, headers=self.headers)
        self.headers['x-xsrf-token'] = response.json()['data']['st']

    # 访问主页的所有帖子
    def get_home_page(self, sleep=.1):
        params = {
            'uid': f'{self.id}',
        }
        resp = self.session.get('https://m.weibo.cn/profile/info', params=params, cookies=self.cookies,
                                headers=self.headers)
        more = resp.json()['data']['more'].split('/')[-1]
        param = {'containerid': more}
        continuations = [param]
        while continuations:
            continuation = continuations.pop()
            message = self.ajax_requests(continuation)
            if message:
                # 模拟向下滑动的操作
                info = message['data']['cardlistInfo']
                i = info.get('since_id')
                p = info.get('page_type')
                if i and p:
                    param['since_id'] = i
                    param['page_type'] = p
                    continuations.append(param)
            datas = message['data']['cards']
            for data in datas:
                t = data['card_type']
                if t == 9:
                    yield from self.typeOf_9(data)
                elif t == 11:
                    yield from self.typeOf_11(data)
            time.sleep(sleep)

    # 用于发出获取相册的ajax请求，重试次数为5次，连续尝试5次之后图片信息为空视为图片爬取结束
    def ajax_request(self, params, retries=5, sleep=5):
        for _ in range(retries):
            response = self.session.get(self.urls, params=params, headers=self.headers, cookies=self.cookies)
            if response.json()['ok']:
                time.sleep(.5)
                return response.json()
            else:
                response = self.session.get('https://m.weibo.cn/api/config', cookies=self.cookies, headers=self.headers)
                self.headers['x-xsrf-token'] = response.json()['data']['st']
                print(f'retrying {_ + 1}/5...')
                time.sleep(sleep)

    # 获取图片的url
    def get_pics(self, sleep=.5):
        params = {
            'uid': f'{self.id}',
        }
        resp = self.session.get('https://m.weibo.cn/profile/info', params=params, cookies=self.cookies,
                                headers=self.headers)
        match_obj = re.search(r'containerid=(\d+)_', resp.json().get('data', {}).get('fans', ''))
        containerid = match_obj.group(1)
        params['containerid'] = containerid
        resp1 = self.session.get('https://m.weibo.cn/api/container/getIndex', params=params, cookies=self.cookies,
                                 headers=self.headers)
        data = resp1.json().get('data', {}).get('tabsInfo', {}).get('tabs')[-1].get('containerid')
        params['containerid'] = data
        resp2 = self.session.get('https://m.weibo.cn/api/container/getIndex', params=params, cookies=self.cookies,
                                 headers=self.headers)
        url = resp2.json()["data"]["cards"][0]["scheme"]
        query = urlparse(str(url)).query
        datas = parse_qs(query)
        params = {
            'containerid': datas['containerid'][0],
            'count': datas['count'][0],
            'title': datas['title'][0],
            'luicode': datas['luicode'][0],
            'lfid': datas['lfid'][0],
        }
        continuations = [params]
        while continuations:
            continuation = continuations.pop()
            info = self.ajax_request(continuation)
            if info:
                if info['ok']:
                    params['containerid'] = info['data']['cardlistInfo']['containerid']
                    params['title'] = info['data']['cardlistInfo']['title']
                    params['page'] = info['data']['cardlistInfo']['page']
                    continuations.append(params)
                datas = info['data']['cards']
                for i in datas:
                    for url in i['pics']:
                        yield url['pic_mw2000']
            time.sleep(sleep)

    # 保存图片至本地
    def save_img(self):
        pics = self.get_pics()
        b = source_downloader()
        # 使用多线程下载
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = []
            count = 0
            for pic in pics:
                count += 1
                # 每添加100个任务提示
                if count % 100 == 0:
                    print(count)
                future = executor.submit(b.download, pic)
                futures.append(future)
            for future in futures:
                future.result()
            executor.shutdown()


if __name__ == '__main__':
    a = user(id)
    items = a.get_home_page()
    for i in items:
        print(i)
