import time
import requests
from os import path, mkdir
from requests.exceptions import RequestException


class source_downloader:
    def __init__(self):
        self.headers = {
            'authority': 'wx3.sinaimg.cn',
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://m.weibo.cn/',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        # 默认保存资源目录，可根据需求自行修改
        if not path.exists('./sourceLib'):
            mkdir('./sourceLib')

    # 下载图片或视频资源，重试次数5次，超时时间15秒
    def download(self, url, retry_times=5):
        _ = url.split('.')[-1]
        n = url.split('/')[-1]
        if _ not in ['jpg', 'gif']:
            p = f'./sourceLib/{n[0:10]}.mp4'
        else:
            p = f'./sourceLib/{n}'
        for i in range(retry_times):
            try:
                resp = requests.get(url, headers=self.headers, timeout=15)
                with open(p, 'wb') as fp:
                    fp.write(resp.content)
                return True
            except RequestException as e:
                print(f"\nDownload failed({e}), retrying ({i + 1}/{retry_times})...\n")
                time.sleep(5)
        # 重试5次之后还未超过，打印出异常的url，可在任务结束后自行手动爬取
        print(f"Failed to download {url} after {retry_times} retries.")
