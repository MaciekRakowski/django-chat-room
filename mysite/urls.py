from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

import SimpleChatApplication.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', SimpleChatApplication.views.index, name='index'),
    url(r'^Logout', SimpleChatApplication.views.Logout, name='Logout'),
    url(r'^DrawLineEvent$', SimpleChatApplication.views.DrawLineEvent, name='DrawLineEvent'),
	url(r'^ShowChatRooms$', SimpleChatApplication.views.ShowChatRooms, name='ShowChatRooms'),
    url(r'^login$', SimpleChatApplication.views.login, name='login'),
	url(r'^PushMessages', SimpleChatApplication.views.PushMessages, name='PushMessages'),
    url(r'^admin/', include(admin.site.urls)),
)
