from rest_framework import serializers

from article.models import Article
from user.serializers import FriendSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class ArticleSerializer(serializers.ModelSerializer):
    author = FriendSerializer(many=False, read_only=True)
    author_pk = serializers.SlugRelatedField(
        source='place', queryset=User.objects.all(), slug_field='pk', write_only=True
    )

    class Meta:
        model = Article
        fields = ['public_id',
                  'title',
                  'description',
                  'image',
                  'author',
                  'author_pk']
        read_only_fields = ['public_id']
