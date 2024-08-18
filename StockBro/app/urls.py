

from django.urls import path
from . import views as app_views
app_name = "stock-app"
urlpatterns = [

    path('', app_views.stock_select, name="select-stocks"),
    path('stock-track', app_views.stock_track, name="track-stocks")

]
