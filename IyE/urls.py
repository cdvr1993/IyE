from django.conf.urls import patterns, include, url
# from django.contrib import admin

urlpatterns = patterns('',
                       url(r'/?^$', 'IyE.views.index'),
    # Examples:
    # url(r'^$', 'IyE.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)
