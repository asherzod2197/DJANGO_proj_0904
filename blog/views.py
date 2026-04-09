# views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Master, Mentor, Group, Student
from .serializers import MasterSerializer, MentorSerializer, GroupSerializer, StudentSerializer


class MasterViewSet(viewsets.ModelViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    search_fields = ['subject']
    ordering_fields = ['subject']
    ordering = ['subject']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def mentors(self, request, pk=None):
        master = self.get_object()
        serializer = MentorSerializer(master.mentors.all(), many=True)
        return Response(serializer.data)


class MentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['master', 'master__subject']
    search_fields = ['firstname', 'lastname']
    ordering_fields = ['firstname', 'lastname']
    ordering = ['firstname']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def groups(self, request, pk=None):
        mentor = self.get_object()
        serializer = GroupSerializer(mentor.groups.all(), many=True)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['mentor']
    search_fields = ['title']
    ordering_fields = ['title']
    ordering = ['title']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['grade']
    search_fields = ['firstname', 'lastname']
    ordering_fields = ['firstname', 'grade']
    ordering = ['firstname']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def by_grade(self, request):
        """Sinf bo'yicha o'quvchilarni ko'rsatish yoki statistika"""
        grade = request.query_params.get('grade')
        if grade:
            students = self.queryset.filter(grade=grade)
            serializer = self.get_serializer(students, many=True)
            return Response(serializer.data)

        from django.db.models import Count
        stats = Student.objects.values('grade').annotate(count=Count('id')).order_by('grade')
        return Response({"stats": list(stats)})