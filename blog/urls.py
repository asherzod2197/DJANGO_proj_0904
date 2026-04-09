# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MasterViewSet, MentorViewSet, GroupViewSet, StudentViewSet

router = DefaultRouter()
router.register(r'masters', MasterViewSet, basename='master')
router.register(r'mentors', MentorViewSet, basename='mentor')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
]