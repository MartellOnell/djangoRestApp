from django.urls import path
from car import views

# add path of comments that base 
# on current car id
# and undercomment that base on current
# comment id on current car id
urlpatterns = [
    path('cars/', views.car_list, name='carList'), # get car list for all users
    path('car/', views.car_create, name='carCreate'), # create car obj
    path('<int:upk>/car/<int:pk>/', views.car_obj, name='carObj'),
    # ^^ put, delete and get car (for owner)
    path('car/<int:pk>/', views.car_obj_spectate, name='carObjSpect'),
    # ^^ get car for all users
    path('car/<int:car_pk>/comments/', views.comment_list, name='comList'),
    # ^^ get comm list on current car (car_pk == current car id)
    # for all users
    path('car/<int:car_pk>/comment/', views.comment_create, name='comCreate'),
    # ^^ create comm on current car (car_pk == current car id)
    path(
        '<int:upk>/car/<int:car_pk>/comment/<int:pk>/', 
        views.comment_obj, 
        name='comObj',
    ),
    # ^^ put, delete and get comm (for owner), (pk == current comm id)
    path(
        'car/<int:car_pk>/comment/<int:comm_pk>/undercomments/', 
        views.undercomment_list, 
        name='ucomList',
    ),
    # ^^ get undercomms list on current comm (comm_pk == current com id)
    # for all users
    path(
        'car/<int:car_pk>/comment/<int:comm_pk>/undercomment/',
        views.undercomment_create,
        name='ucomCreate'
    ),
    # ^^ create undercomm on current comm
    path(
        '<int:upk>/car/<int:car_pk>/comment/<int:comm_pk>/undercomment/<int:pk>',
        views.undercomment_obj,
        name='ucomObj',
    )
    # ^^ put, delete and get undercomm (for owner), (pk == current undercomm id)
]