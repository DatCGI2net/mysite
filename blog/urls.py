from django.conf.urls import url
from . import views
#from django.contrib.auth import views as auth_views

urlpatterns = [

url(r'^blog/login/$',views.login_user, name='login'),
url(r'^blog/logout/$',views.logout_user,name='logout'),
url(r'^tag/(?P<tagSlug>[a-zA-Z0-9]+)/$', views.TagView.as_view(), name='tags'),
url(r'^category/(?P<categorySlug>[a-zA-Z0-9]+)/$', views.CategoryView.as_view(), name='category'),
url(r'^blog/(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
url(r'^blog/(?P<postSlug>[a-zA-Z0-9]+)/$', views.getPost, name='detail'),
url(r'^blog/(?P<post_id>[0-9]+)/comments/$', views.comments, name='comments'),
url(r'^blog/(?P<post_id>[0-9]+)/comment/$', views.comment, name='comment'),

url(r'^blog', views.index, name='home'),
url(r'^$', views.index, name='home'),



]
