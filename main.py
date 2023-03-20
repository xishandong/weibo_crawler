from get_comments.get_comments import comment_downloader
from search_key.search_key import searchKey
from download.download import source_downloader
from search_user.search_user import user


if __name__ == '__main__':
    # 此处只展示如何实例化类， 不同的类初始化条件不同
    uid = input('输入uid: ')
    mid = input('输入mid: ')
    c = comment_downloader(mid)
    a = searchKey()
    s = source_downloader()
    u = user(uid)
