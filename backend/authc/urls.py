from django.urls import path
from . import views
# using .../profile/?upid=<int> to path profile

urlpatterns = [
    path('login/', views.login, name='userLogin'),
    # ^^ only POST method (data to input: email, password)
    path('register/', views.register_send_mail, name='regPartMailSend'),
    # ^^ only POST method (data to input: username, email, password)
    path('register/verify/<str:token>/', views.register_final_verify, name='regPartMailVer'),
    # ^^ only GET method 
    # (if reg was succ returned json response "user succ created")
    path('<int:upk>/profile/', views.profile, name='profile'),
]