from django.urls import path

from scanhosts import views
from django.views.decorators.cache import cache_page

app_name = 'scanhosts'

urlpatterns = [
    path("sendinfos", views.user_info, name='sendinfos')
]
