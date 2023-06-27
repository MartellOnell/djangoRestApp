from rest_framework.serializers import (
    Serializer,
    CharField,
    EmailField,
    IntegerField,
)


# !!!!!! serializer doesn`t inherit functions of model
# check https://krakensystems.co/blog/2020/custom-users-using-django-rest-framework
# to finnaly write user model and user serializer !!!!
class UserSerializer(Serializer):
    id = IntegerField()
    email = EmailField()
    username = CharField(max_length=40)
    password = CharField(max_length=128)
