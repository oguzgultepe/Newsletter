from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submit/$', views.submit, name= 'submit'),
    url(r'^submission/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name= 'detail'),
    url(r'^user/$', views.user, name= 'user'),
    url(r'^submission/(?P<pk>[0-9]+)/edit/$',views.edit, name= 'edit'),
    url(r'^display/$', views.display, name= 'display'),
    url(r'^index/$', views.index, name= 'index'),
    url(r'^unsubscribe/(?P<pk>[0-9]+)/$', views.unsubscribe, name='unsubscribe'),
    url(r'^send/$', views.send, name= 'send'),
    url(r'^send/newsletter/$', views.send_newsletter, name='send_newsletter'),
    url(r'^send/reminder/$', views.send_reminder, name= 'send_reminder'),
]
