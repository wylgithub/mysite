from django.conf.urls import patterns, include, url
from django.contrib import admin
from books import views
from mysite.views import hello, current_datetime, hours_ahead, display_meta, printInfo
from books.models import Publisher


publisher_info = {
    'queryset': Publisher.objects.all(),
}


urlpatterns = patterns('',

    ('^hello/$', hello),
    url(r'^admin/', include(admin.site.urls)),
    ('^time/$', current_datetime),
    ('^meta/$', display_meta),
    (r'^time/plus/(\d{1,2})/$', hours_ahead),
    # (r'^search-form/$', views.search_form),
    (r'^search/$', views.search),
    (r'^contact/$', views.contact),
    (r'^printinfo/$', printInfo),
)

