from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('apps.dashboard_app.urls')),
]
