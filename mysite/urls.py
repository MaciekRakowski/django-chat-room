from django.conf.urls import patterns, include, url
from django.contrib import admin

import hello.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', hello.views.index, name='index'),
	url(r'^RegisterPusher', hello.views.RegisterPusher, name='RegisterPusher'),
    url(r'^admin/', include(admin.site.urls)),
)
