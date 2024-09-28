from rest_framework import serializers

from article.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['public_id',
                  'title',
                  'description',
                  'image']
        read_only_fields = ['public_id']
