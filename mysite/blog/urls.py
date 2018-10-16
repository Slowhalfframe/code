from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^user_add/$', views.user_add, name='user_add'),
    # url(r'^ok/$', views.ok, name='ok'),
    url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^user_info/(\d+)/$', views.user_info, name='user_info'),
    url(r'^del_user/(?P<u_id>\d+)/$', views.del_user, name='del_user'),
    url(r'^update_user/(?P<u_id>\d+)/$', views.update_user, name='update_user'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^user_logout/$', views.user_logout, name='user_logout'),
    url(r'^update_self/$', views.update_self, name="update_self"),
    url(r'^update_user_header/(?P<u_id>\d+)/$', views.update_user_header, name="update_user_header"),

    url(r'^code/$', views.code, name='code'),

    # 文章
    url(r'^add_article/$', views.add_article, name='add_article'),
    # url(r'^show_article/$', views.show_article, name='show_article'),
    url(r'^article_content/(\d+)/$', views.article_content, name='article_content'),
    url(r'^article_list/$', views.article_list, name='article_list'),
    url(r'^del_article/(?P<a_id>\d+)/$', views.del_article, name='del_article'),
    url(r'^article_top/(?P<a_id>\d+)/$', views.article_top, name='article_top'),
    url(r'^article_del_top/(?P<a_id>\d+)/$', views.article_del_top, name='article_del_top'),
    url(r'^article_del_res/(?P<a_id>\d+)/$', views.article_del_res, name='article_del_res'),
    url(r'^update_article/(?P<a_id>\d+)/$', views.update_article, name='update_article'),
    url(r'^main/$', views.main, name='main'),
    url(r'^user/(\d+)/$', views.user, name='user'),
    url(r'^yuanchuang/', views.yuanchuang, name='yuanchuang'),
    url(r'^banyun/', views.banyun, name='banyun'),
    url(r'^other/', views.other, name='other'),
    url(r'^del_article_list/', views.del_article_list, name='del_article_list'),


    url(r'^(\w+)/checkusername/$', views.checkusername, name='checkusername'),
    # url(r'^(\w+)/checkpassword/$', views.checkpassword, name='checkpassword'),

]