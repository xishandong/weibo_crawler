import requests
import time
import csv


class comment_downloader:
    def __init__(self, id):
        self.session = requests.Session()
        self.headers = {
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'MWeibo-Pwa': '1',
            'referer': 'https://m.weibo.cn/',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.url = 'https://m.weibo.cn/comments/hotflow'
        self.id = id
        self.cookies = {
            '__bid_n': 填你的cookie,
            'FPTOKEN': 填你的cookie,
            'WEIBOCN_FROM': 填你的cookie,
            'SUB': 填你的cookie,
            '_T_WM': 填你的cookie,
            'BAIDU_SSP_lcr': 'https://security.weibo.com/',
            'M_WEIBOCN_PARAMS': f'oid%3D{id}%26luicode%3D20000061%26lfid%3D{id}%26uicode%3D20000061%26fid%3D{id}',
        }
        response = self.session.get('https://m.weibo.cn/api/config', cookies=self.cookies, headers=self.headers)
        self.headers['x-xsrf-token'] = response.json()['data']['st']

    # 用于发送ajax请求，重试次数为5次
    def ajax_requests(self, params, retries=5, sleep=5):
        for _ in range(retries):
            response = self.session.get(self.url, params=params, headers=self.headers, cookies=self.cookies)
            if response.json()['ok']:
                time.sleep(.5)
                return response.json()
            else:
                response = self.session.get('https://m.weibo.cn/api/config', cookies=self.cookies, headers=self.headers)
                self.headers['x-xsrf-token'] = response.json()['data']['st']
                print(f'retrying {_ + 1}/5...')
                time.sleep(sleep)

    # 获取评论
    def get_comment_by_id(self):
        params0 = {
            'id': f'{self.id}',
            'mid': f'{self.id}',
            'max_id_type': '0',
        }
        continuations = [params0]
        while continuations:
            continuation = continuations.pop()
            resp = self.ajax_requests(continuation)
            if resp:
                # 模拟手指向下滑动
                if resp['data']['max_id'] != 0:
                    params1 = {
                        'id': f'{self.id}',
                        'mid': f'{self.id}',
                        'max_id': f"{resp['data']['max_id']}",
                        'max_id_type': f'{resp["data"]["max_id_type"]}',
                    }
                    continuations.append(params1)
                datas = resp['data']['data']
                if datas:
                    for data in datas:
                        yield from self.get_dic(data)
                        comments = data.get('comments')
                        if comments:
                            for comment in comments:
                                yield from self.get_dic(comment)

    # 将评论保存至csv文件
    def save2CSV(self):
        items = self.get_comment_by_id()
        header = ['comment_id', 'user_id', 'user_name', 'text', 'liked', 'location', 'time']
        fp = open(f'{self.id}.csv', 'w', encoding='utf-8', newline='')
        writer = csv.DictWriter(fp, header)
        writer.writeheader()
        flag = 0
        for i in items:
            flag += 1
            if flag % 100 == 0:
                print(f'写入{flag}条数据')
            writer.writerow(i)

    @staticmethod
    def get_dic(data):
        created_at = data['created_at']
        comment_id = data['id']
        text = data['text']
        like = data.get('like_count')
        user_name = data['user']['screen_name']
        user_id = data['user']['id']
        source = data.get('source')
        item = {
            'comment_id': comment_id,
            'user_id': user_id,
            'user_name': user_name,
            'text': text,
            'liked': like,
            'location': source,
            'time': created_at
        }
        yield item


if __name__ == '__main__':
    c = comment_downloader(mid)
    items = c.get_comment_by_id()
    for i in items:
        print(i)
