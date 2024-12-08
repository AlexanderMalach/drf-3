from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from users.permissions import IsModerator, IsOwner
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseCreateAPIView(CreateAPIView):
    """
    Создание курсов только для владельцев.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Присваиваем владельца при создании курса
        serializer.save(owner=self.request.user)


class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD операции для курсов с проверкой прав.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Модераторы видят все курсы, пользователи — только свои
        if self.request.user.groups.filter(name='Moderator').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Запрет на создание курсов для модераторов
        if self.request.user.groups.filter(name='Moderator').exists():
            raise PermissionDenied("Модераторы не могут создавать курсы.")
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        # Запрет на удаление курсов для модераторов
        if self.request.user.groups.filter(name='Moderator').exists():
            raise PermissionDenied("Модераторы не могут удалять курсы.")
        instance.delete()


class LessonViewSet(viewsets.ModelViewSet):
    """
    CRUD операции для уроков с проверкой прав.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Модераторы видят все уроки, пользователи — только свои
        if self.request.user.groups.filter(name='Moderator').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Запрет на создание уроков для модераторов
        if self.request.user.groups.filter(name='Moderator').exists():
            raise PermissionDenied("Модераторы не могут создавать уроки.")
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        # Запрет на удаление уроков для модераторов
        if self.request.user.groups.filter(name='Moderator').exists():
            raise PermissionDenied("Модераторы не могут удалять уроки.")
        instance.delete()


class LessonListCreateView(ListCreateAPIView):
    """
    Список и создание уроков.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Присваиваем владельца при создании урока
        serializer.save(owner=self.request.user)


class LessonDetailView(RetrieveUpdateDestroyAPIView):
    """
    Детальный просмотр, обновление и удаление урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
