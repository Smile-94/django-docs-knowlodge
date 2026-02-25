from django.urls import path

from apps.user.views.login_view import TokenObtainView, TokenRefreshView
from apps.user.views.registration_view import RegistrationView

# <<--------------------------------- User URLs --------------------------------->>
urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
]

# <<--------------------------------- Authentication URLs --------------------------------->>
urlpatterns += [
    path("login/", TokenObtainView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
]
