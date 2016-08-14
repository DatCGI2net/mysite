from django.conf.urls import url
from . import views
#from django.contrib.auth import views as auth_views

urlpatterns = [

url(r'^$', views.index, name='home'),
url(r'^login/$',views.login_user, name='login'),
url(r'^logout/$',views.logout_user,name='logout'),
url(r'^tag/(?P<tagSlug>[a-zA-Z0-9\-_]+)/$', views.TagView.as_view(), name='tags'),
url(r'^category/(?P<categorySlug>[a-zA-Z0-9\-_]+)/$', views.CategoryView.as_view(), name='category'),
url(r'^(?P<post_id>[0-9]+)/$', views.detail, name='detail'),
url(r'(?P<postSlug>[a-zA-Z0-9\-_]+)/$', views.getPost, name='detail'),
url(r'^(?P<post_id>[0-9]+)/comments/$', views.comments, name='comments'),
url(r'^(?P<post_id>[0-9]+)/comment/$', views.comment, name='comment'),


url(r'^blog/?$', views.index, name='home'),


]
