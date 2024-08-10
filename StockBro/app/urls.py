

from django.urls import path
from . import views as app_views

urlpatterns = [

    path('', app_views.home, name="homepage")
]
