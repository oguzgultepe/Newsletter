from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submit/$', views.submit, name= 'submit'),
    url(r'^submission/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name= 'detail'),
    url(r'^user/$', views.user, name= 'user'),
    url(r'^send/$', views.send, name= 'send'),
    url(r'^submission/(?P<pk>[0-9]+)/edit/$',views.edit, name= 'edit'),
    url(r'^display/$', views.display, name= 'display'),
    url(r'^index/$', views.index, name= 'index'),
]
