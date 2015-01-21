from django.conf.urls import patterns, include, url
from django.contrib import admin
from books import views
from mysite import settings
from mysite.views import hello, current_datetime, hours_ahead, display_meta



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    ('^hello/$', hello),
    url(r'^admin/', include(admin.site.urls)),
    ('^time/$', current_datetime),
    ('^meta/$', display_meta),
    (r'^time/plus/(\d{1,2})/$', hours_ahead),
    # (r'^search-form/$', views.search_form),
    (r'^search/$', views.search),
    (r'^contact/$', views.contact),


)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^debuginfo/$', views.debug),
    )

