# weibo全站数据下载

***
# 做了一个集成，直接使用merge.py即可，其余可不用管
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

见merge.py中的注释

## WARNING

***

除了搜索框搜索功能外，其他所有功能需要手动将cookies贴到相关类的初始化中

可以只用代码中罗列出来的cookie项

手动粘贴的cookie时效为1年
