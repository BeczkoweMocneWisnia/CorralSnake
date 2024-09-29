from django.urls import path

from quiz.views import QuizViewSet, QuestionViewSet, QuestionAnswerViewSet, SubmittedQuestionViewSet

urlpatterns = [
    path('', QuizViewSet.as_view({'post': 'create'})),
    path('<uuid:public_id>/', QuizViewSet.as_view({'get': 'retrieve',
                                                   'put': 'update',
                                                   'patch': 'partial_update',
                                                   'delete': 'destroy'})),
    path('question/', QuestionViewSet.as_view({'post': 'create'})),
    path('question/<uuid:public_id>/', QuestionViewSet.as_view({'get': 'retrieve',
                                                                'put': 'update',
                                                                'patch': 'partial_update',
                                                                'delete': 'destroy'})),
    path('question/answer/', QuestionAnswerViewSet.as_view({'post': 'create'})),
    path('question/answer/<uuid:public_id>/', QuestionAnswerViewSet.as_view({'get': 'retrieve',
                                                                             'put': 'update',
                                                                             'patch': 'partial_update',
                                                                             'delete': 'destroy'})),
    path('question/answer/submit/', SubmittedQuestionViewSet.as_view({'post': 'create'})),
    path('question/answer/submit/<uuid:public_id>/', SubmittedQuestionViewSet.as_view({'get': 'retrieve',
                                                                                       'put': 'update',
                                                                                       'patch': 'partial_update',
                                                                                       'delete': 'destroy'})),
]
