from rest_framework import serializers
from .models import Category


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["id"]
        depth = 1


class ParentCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        read_only_fields = ["id"]
        exclude = ["parent"]


class ParentCategorySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=100)
    children = ParentCategoryModelSerializer(many=True)
