from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^create$', views.create),
    url(r'^dashboard$', views.dashboard),
    url(r'^login_submit$', views.login_submit),
    url(r'^logout$', views.logout_user),
    url(r'^users/show/(?P<id>\d+)$', views.show_one),
    url(r'^users/edit$', views.edit),
    url(r'^update$', views.update),
    url(r'^update_pw$', views.update_pw),
    url(r'^update_desc$', views.update_desc),
    url(r'^users/(?P<id>\d+)/create_post$', views.create_post),
    url(r'^users/(?P<user_id>\d+)/post/(?P<post_id>\d+)/create_comment$', views.create_comment),
    url(r'^dashboard/admin$', views.admin_dashboard),
    url(r'^users/(?P<id>\d+)/delete$', views.delete),
    url(r'^users/(?P<id>\d+)/edit$', views.admin_edit),
    url(r'^users/(?P<id>\d+)/update$', views.admin_update),
    url(r'^users/(?P<id>\d+)/update_pw$', views.admin_update_pw),
    url(r'^users/new$', views.new_user),
    url(r'^admin/create_user$', views.create_user),
]
