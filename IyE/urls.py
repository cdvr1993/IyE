from django.conf.urls import patterns, include, url
# from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', 'IyE.views.index'),
                       url(r'^user/login$', 'IyE.views.login'),
                       url(r'^user/new$', 'IyE.views.register'),
                       url(r'^user/info$', 'IyE.views.user_info'),
                       url(r'^contact$', 'IyE.views.contact'),
                       url(r'^about$', 'IyE.views.about'),
                       url(r'^cart$', 'IyE.views.cart'),
                       url(r'^pay$', 'IyE.payments.pay'),
)
