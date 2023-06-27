from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
)
from .models import Car, Comment, UnderComment


class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'user_id', 'company_name', 'model_name', 'content']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'car_id', 'rate', 'content']


class UnderCommentSerializer(ModelSerializer):
    class Meta:
        model = UnderComment
        fields = ['id', 'user_id', 'comm_id', 'car_id', 'content']
        