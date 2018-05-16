"""hopper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from hopper import views

from hopper.settings import HOPPER_PASSWORD

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/events/$', views.EventList.as_view()),
    url(r'^api/v1/rooms/$', views.RoomList.as_view()),
    url(r'^api/v1/events/(?P<pk>.*)$', views.EventDetail.as_view()),
    url(r'^api/v1/rooms/(?P<pk>.*)$', views.RoomDetail.as_view()),
    url(r'^compare/(?P<pk>.*)$', views.compare_view, name='compare-complete'),
    url(r'^{}/export.xml$'.format(HOPPER_PASSWORD), views.xml),
    url(r'^sched.csv$', views.sched),
    url(r'^confirm.html$',views.confirm_emails),
    url(r'^run.html$',views.runner_instructions),
    url(r'^$', views.index),
    ]
