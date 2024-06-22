from django.urls import path
from .views import *
from . import views
from . import api
from rest_framework.authtoken.views import obtain_auth_token  # Add this import

# I wrote this code

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("user/<str:username>/", views.user_home, name="user_home"),
    path(
        "send_friend_request/<int:user_id>/",
        send_friend_request,
        name="send_friend_request",
    ),
    path(
        "accept_friend_request/<int:request_id>/",
        accept_friend_request,
        name="accept_friend_request",
    ),
    path(
        "decline_friend_request/<int:request_id>/",
        views.decline_friend_request,
        name="decline_friend_request",
    ),
    path("chat/<str:room_name>/", views.room, name="room"),
    path("user/<str:username>/api/user/", api.user_detail, name="user_api"),
    path("api/token/", obtain_auth_token, name="obtain_auth_token"),
]


# end of code I wrote
