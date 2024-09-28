from django.urls import path

from quiz.views import QuizViewSet, QuestionViewSet, QuestionAnswerViewSet

urlpatterns = [
    path('', QuizViewSet.as_view({'post': 'create',
                                  'get': 'retrieve',
                                  'put': 'update',
                                  'patch': 'partial_update',
                                  'delete': 'destroy'})),
    path('question', QuestionViewSet.as_view({'post': 'create',
                                              'get': 'retrieve',
                                              'put': 'update',
                                              'patch': 'partial_update',
                                              'delete': 'destroy'})),
    path('question/answer', QuestionAnswerViewSet.as_view({'post': 'create',
                                                           'get': 'retrieve',
                                                           'put': 'update',
                                                           'patch': 'partial_update',
                                                           'delete': 'destroy'})),
]
