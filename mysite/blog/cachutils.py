from django.core.cache import cache

from . import models

def getAllArticles(ischange = False):
    # 首先，从缓存中去查找数据
    print("首先开始查询数据")
    print("从缓存中查询数据")
    articles = cache.get("allArticle")
    if articles == None or ischange == True:
        print("没有数据，查询数据库中的")
        articles = models.Article.objects.filter(type=1).order_by("-publish_time")
        print("查到了数据，保存到缓存中")
        cache.set("allArticle", articles)

    return articles
