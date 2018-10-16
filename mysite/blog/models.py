from django.db import models

from DjangoUeditor.models import UEditorField



# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True),
    username = models.CharField(max_length=56, verbose_name="用户用户名")
    password = models.CharField(max_length=256, verbose_name="用户密码")
    name = models.CharField(max_length=99, verbose_name="用户姓名")
    age = models.IntegerField(default=19, verbose_name="用户年龄")
    email = models.EmailField(max_length=256, verbose_name="用户邮箱")
    type = models.IntegerField(default=0, verbose_name="用户级别，0普通会员，1超级管理")
    header = models.ImageField(upload_to='static/headers/', default='static/images/headers/default.png', verbose_name="用户头像")
    self_info = models.CharField(max_length=256, default="还没有设置个性签名", verbose_name="用户的个性签名")
    article_num = models.IntegerField(default=0,verbose_name="发表文章的数量")

    def __str__(self):
        return self.username


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="文章标题")
    note = models.CharField(max_length=256, verbose_name="内容摘要")
    # content = models.TextField(verbose_name="文章内容")
    content = UEditorField(verbose_name="文章内容")
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    count = models.IntegerField(default=0, verbose_name="点击量")
    image = models.ImageField(upload_to='static/articles/header_image', null=True, verbose_name="文章封面图片")
    # 外键
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 文章类型 默认= 1 一般文章，2 置顶文章， 0 隐藏（删除）文章
    type = models.IntegerField(default=1, verbose_name="文章状态")
    # 文章分类 1==搬运 2==原创 3==其它  默认其他
    feilei = models.IntegerField(default=3, verbose_name="文章的分类")

    def __str__(self):
        return self.title