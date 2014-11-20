from django.conf.urls import patterns, include, url
# from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^about$', 'IyE.views.about'),
                       url(r'^cart/show$', 'IyE.views.cart_show'),
                       url(r'^cart/checkout$', 'IyE.views.checkout'),
                       url(r'^contact$', 'IyE.views.contact'),
                       url(r'^colors$', 'IyE.views.get_colors'),
                       url(r'^pay$', 'IyE.payments.pay'),
                       url(r'^product/detail$', 'IyE.views.product_detail'),
                       url(r'^$', 'IyE.views.index'),
                       url(r'^user/login$', 'IyE.views.login'),
                       url(r'^user/logout$', 'IyE.views.logout'),
                       url(r'^user/new$', 'IyE.views.register'),
                       url(r'^user/info$', 'IyE.views.user_info'),
)
