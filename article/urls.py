from django.urls import path

from article.views import ArticleViewSet

urlpatterns = [
    path('', ArticleViewSet.as_view({'post': 'create',
                                     'get': 'retrieve',
                                     'put': 'update',
                                     'patch': 'partial_update',
                                     'delete': 'destroy'})),

    path('search/', ArticleViewSet.as_view({'get': 'list'})),
]
