from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submit/$', views.submit, name= 'submit'),
    url(r'^display/$', views.display, name= 'display'),
    url(r'^user/$', views.user, name= 'user'),
    url(r'^send/$', views.send, name= 'send'),
    url(r'^edit/$', views.edit, name= 'edit'),
]
