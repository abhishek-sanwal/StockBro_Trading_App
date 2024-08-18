
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import signup

app_name = "authy"
urlpatterns = [
    path('login/', LoginView.as_view(template_name="authy/login.html"),
         name="login"),
    path('logout/', LogoutView.as_view(template_name="authy/logout.html"),
         name="logout"),
    path('signup/', signup, name="signup")
]
