import time
import requests


class searchKey:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'MWeibo-Pwa': '1',
            'Referer': 'https://m.weibo.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.url = 'https://m.weibo.cn/api/container/getIndex'

    # 用于发出ajax请求，设置重试次数为5
    def ajax_requests(self, params, retries=5, sleep=5):
        for _ in range(retries):
            response = self.session.get(self.url, params=params, headers=self.headers)
            if response.json()['ok']:
                return response.json()
            else:
                print(f'retry {_ + 1}/5...')
                time.sleep(sleep)

    def search(self, key, sleep=.5):
        num = 1
        params0 = {
            'containerid': f'100103type=1&q={key}',
            'page_type': 'searchall',
        }
        while True:
            if num == 1:
                params = params0
            else:
                # 模拟翻页操作
                params = {
                    'containerid': f'100103type=1&q={key}',
                    'page_type': 'searchall',
                    'page': f'{num}'
                }
            message = self.ajax_requests(params)
            if not message:
                break
            datas = message['data']['cards']
            for data in datas:
                t = data['card_type']
                if t == 9:
                    yield from self.typeOf_9(data)
                elif t == 11:
                    yield from self.typeOf_11(data)
            num += 1
            time.sleep(sleep)

    # 获取模式为11下的帖子
    def typeOf_11(self, m):
        cs = m['card_group']
        for c in cs:
            t = c['card_type']
            if t == 9:
                yield from self.typeOf_9(c)

    # 获取模式为9下面的文章
    @staticmethod
    def typeOf_9(m):
        mlog = m['mblog']
        id = mlog['id']
        mid = mlog['mid']
        region_name = mlog.get('status_province')
        time = mlog.get('created_at')
        text = mlog['text']
        author = mlog['user']['screen_name']
        author_fans = mlog['user']['followers_count']
        page_info = mlog.get('page_info')
        info = None
        if page_info:
            info = {
                'cover': page_info.get('page_pic')['url'],
                'media_url': page_info.get('urls')
            }
        try:
            pic = [d['url'] for d in mlog['pics']]
        except KeyError:
            pic = None
        try:
            video = [d['videoSrc'] for d in mlog['pics']]
        except KeyError:
            video = None
        item = {
            'time': time,
            'id': id,
            'mid': mid,
            'region_name': region_name,
            'text': text,
            'author': author,
            'author_fans': author_fans,
            'pic': pic,
            'video': video,
            'page_info': info
        }
        yield item


if __name__ == '__main__':
    # 一个例子，展示实时搜索框内容
    s = searchKey()
    items = s.search('IU')
    for i in items:
        print(i)
