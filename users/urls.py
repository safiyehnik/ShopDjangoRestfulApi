from users.views.sign_up_view import SignUpView
from django.urls import  re_path


urlpatterns = [
    re_path(r'sign_up', SignUpView.as_view())

]

