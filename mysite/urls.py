from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

import hello.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', hello.views.index, name='index'),
    url(r'^Logout', hello.views.Logout, name='Logout'),
    url(r'^DrawLineEvent$', hello.views.DrawLineEvent, name='DrawLineEvent'),
	url(r'^ShowChatRooms$', hello.views.ShowChatRooms, name='ShowChatRooms'),
    url(r'^login$', hello.views.login, name='login'),
    url(r'^db$', hello.views.db, name='db'),
	url(r'^RegisterPusher', hello.views.RegisterPusher, name='RegisterPusher'),
    url(r'^admin/', include(admin.site.urls)),
)
