# weibo全站数据下载

***

## 支持功能

***

1.  搜索框搜索关键词的帖子详情内容
2.  用户主页帖子详情内容
3.  用户相册所有图片下载
4.  指定帖子所有评论下载

# Install

***

```python
pip install requests
```

# 使用示例

### 搜索关键词展示帖子

```python
from search_key.search_key import searchKey


s = searchKey()
    items = s.search('IU')
    for i in items:
        print(i)
```

### 指定用户查看帖子

```python
from search_user.search_user import user


a = user(uid)
items = a.get_home_page()
for i in items:
	print(i)
```

### 指定用户下载相册所有内容

```python
from search_user.search_user import user

a = user(uid)
a.save_img()
```

### 查看指定帖子评论以及下载

```python
from get_comments.get_comments import comment_downloader

# 查看
c = comment_downloader(mid)
items = c.get_comment_by_id()
for i in items:
	print(i)

# 保存
c.save2CSV()
```

## WARNING

***

除了搜索框搜索功能外，其他所有功能需要手动将cookies贴到相关类的初始化中

可以只用代码中罗列出来的cookie项

手动粘贴的cookie时效为1年
