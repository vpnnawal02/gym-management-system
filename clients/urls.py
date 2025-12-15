from django.urls import path
from .views import *

urlpatterns = [
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("add/", add_client, name="add_client"),
    path("renew_membership/", renew_membership),
    path("remove_client/", remove_client),
]
