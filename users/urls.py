from users.views.profile_view import ProfileView
from users.views.sign_up_view import SignUpView
from django.urls import re_path


urlpatterns = [
    re_path(r'sign_up', SignUpView.as_view()),
    re_path(r'users/(?P<pk>\d+)/profile/?$', ProfileView.as_view({"get": "retrieve", "patch": "partial_update"}))

]

