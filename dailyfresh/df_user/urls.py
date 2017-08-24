from django.conf.urls import url
import views


urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^register_handle/$', views.register_handle, name='register_handle'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_handle/$', views.login_handle, name='login_handle'),
    url(r'^register_exit/$', views.register_exit, name='register_exit'),
    url(r'^info/$', views.info, name='info'),
    url(r'^order(\d*)/$', views.order, name='order'),
    url(r'^site/$', views.site, name='site'),
    url(r'^logout/$', views.logout, name='logout'),

]
