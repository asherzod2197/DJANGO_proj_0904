from django.contrib import admin
from .models import Master, Mentor, Group, Student

# Register your models here.
admin.site.register(Master)
admin.site.register(Mentor)
admin.site.register(Group)
admin.site.register(Student)