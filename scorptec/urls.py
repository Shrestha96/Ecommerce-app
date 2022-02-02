from django.urls import re_path,path
from scorptec import views
#importing view for password reset

app_name = 'scorptec'

urlpatterns=[
    re_path(r'^about/$', views.about, name = 'about'),
    re_path(r'^policy/$', views.policy, name = 'policy'),
    re_path(r'^contact/$', views.contact, name = 'contact'),
    re_path(r'^products/$', views.product, name = 'product'),
    re_path(r'^register/$', views.register, name = 'register'),
    re_path(r'^userhome/$', views.userhome, name = 'userhome'),
    re_path(r'^terms/$', views.terms, name = 'terms'),


    re_path(r'^login/$', views.loginPage, name = 'login'),
    re_path(r'^logout/$', views.logoutUserProfile, name = 'logout'),


    re_path(r'^update_item/$', views.updateItem, name = 'update_item'),
    re_path(r'^my_cart/$', views.myCart, name = 'my_cart'),
    re_path(r'^checkout/$', views.checkout, name = 'checkout'),
    re_path(r'^order_process/$', views.orderProcess, name = 'order_process'),
    re_path(r'^update_favourite/$', views.updateFavourite, name = 'update_favourite'),
    re_path(r'^favourite/$', views.favourite, name = 'favourite'),
    re_path(r'^user_profile/$', views.userProfile, name = 'user_profile'),
    re_path(r'^update_user/$', views.updateUser, name = 'update_user'),

    #SEARCH url
    re_path(r'^search/$', views.search, name="search"),


]
