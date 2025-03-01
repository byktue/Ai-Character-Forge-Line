import re

# 我的设计理念是像html，每个标签<h1>代表对模型的调用，每个标签里可以有样式来对维度上的信息准确化，最终实现一个递归的程序，不同标签之间可以用src连接其他标签。
# 以下HtmlParser应该是对整个html文档树进行构建出真正的model分析调用树
class Node:
    pass


class HtmlParser:
    pass