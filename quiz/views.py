from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from quiz.models import Quiz, QuestionAnswer, Question, SubmittedAnswer
from quiz.serializers import QuizSerializer, QuestionSerializer, QuizFullSerializer, QuestionAnswerSerializer, \
    SubmittedAnswerSerializer
from user.permissions import TeacherOnly


class QuizViewSet(viewsets.ModelViewSet):
    lookup_field = 'public_id'
    queryset = Quiz.objects.all().order_by('id')

    def create(self, request, *args, **kwargs):
        """
        Creates a new quiz. Only accessible by users with the 'TeacherOnly' permission.
        """
        serializer = self.get_serializer(data=request.data | {'author_pk': request.user.pk})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a quiz by its public ID. Any authenticated user can access this.
        """
        quiz = self.get_object()
        serializer = self.get_serializer(quiz)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing quiz. Only the author of the quiz is allowed to update it.
        """
        quiz = self.get_object()
        if quiz.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(quiz, data=request.data | {'author_pk': request.user.pk})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates an existing quiz. Only the author of the quiz is allowed to make changes.
        """
        quiz = self.get_object()
        if quiz.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(quiz, data=request.data | {'author_pk': request.user.pk}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a quiz. Only the author of the quiz is allowed to delete it.
        """
        quiz = self.get_object()
        if quiz.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(quiz)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [TeacherOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuizFullSerializer
        return QuizSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    lookup_field = 'public_id'
    queryset = Question.objects.all().order_by('order')
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a new question. Only accessible by users with the 'TeacherOnly' permission.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a question by its public ID. Any authenticated user can access this.
        """
        question = self.get_object()
        serializer = self.get_serializer(question)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing question. Only the author of the question's quiz is allowed to update it.
        """
        question = self.get_object()
        if question.quiz.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(question, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates an existing question. Only the author of the question's quiz is allowed to make changes.
        """
        question = self.get_object()
        if question.quiz.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(question, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a question. Only the author of the question's quiz is allowed to delete it.
        """
        question = self.get_object()
        if question.quiz.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(question)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [TeacherOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class QuestionAnswerViewSet(viewsets.ModelViewSet):
    lookup_field = 'public_id'
    queryset = QuestionAnswer.objects.all().order_by('id')
    serializer_class = QuestionAnswerSerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a new question answer. Only accessible by users with the 'TeacherOnly' permission.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a question answer by its public ID. Any authenticated user can access this.
        """
        answer = self.get_object()
        serializer = self.get_serializer(answer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing question answer. Only the author of the question's quiz is allowed to update it.
        """
        answer = self.get_object()
        if answer.question.quiz.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(answer, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates an existing question answer. Only the author of the question's quiz is allowed to make changes.
        """
        answer = self.get_object()
        if answer.question.quiz.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(answer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a question answer. Only the author of the question's quiz is allowed to delete it.
        """
        answer = self.get_object()
        if answer.question.quiz.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(answer)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [TeacherOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class SubmittedQuestionViewSet(viewsets.ModelViewSet):
    lookup_field = 'public_id'
    queryset = SubmittedAnswer.objects.all().order_by('id')
    serializer_class = SubmittedAnswerSerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a new question answer. Only accessible by users with the 'TeacherOnly' permission.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def retrieve(self, request, *args, **kwargs):
    #     """
    #     Retrieves a question answer by its public ID. Any authenticated user can access this.
    #     """
    #     answer = self.get_object()
    #     serializer = self.get_serializer(answer)
    #     return Response(serializer.data)
    #
    # def update(self, request, *args, **kwargs):
    #     """
    #     Updates an existing question answer. Only the author of the question's quiz is allowed to update it.
    #     """
    #     answer = self.get_object()
    #     if answer.question.quiz.author != request.user:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)
    #     serializer = self.get_serializer(answer, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)
    #
    # def partial_update(self, request, *args, **kwargs):
    #     """
    #     Partially updates an existing question answer. Only the author of the question's quiz is allowed to make changes.
    #     """
    #     answer = self.get_object()
    #     if answer.question.quiz.author != request.user:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)
    #     serializer = self.get_serializer(answer, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a question answer. Only the author of the question's quiz is allowed to delete it.
        """
        answer = self.get_object()
        if answer.question.quiz.author != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(answer)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [TeacherOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
