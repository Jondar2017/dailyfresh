from django.conf.urls import url
import views
from views import *

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^list(\d+)_(\d+)_(\d+)/$', views.list, name='list'),
    url(r'^(\d+)/$', views.detail, name='detail'),
    url(r'^search/', MySearchView()),

]
