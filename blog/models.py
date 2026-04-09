# models.py
from django.db import models

class Master(models.Model):
    """Fanlar modeli"""
    subject = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
        ordering = ['subject']


class Mentor(models.Model):
    """Mentor (O'qituvchi) modeli"""
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        related_name='mentors'
    )

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = "Mentor"
        verbose_name_plural = "Mentorlar"
        ordering = ['firstname']


class Group(models.Model):
    """Guruh modeli"""
    title = models.CharField(max_length=100, unique=True)
    mentor = models.ForeignKey(
        Mentor,
        on_delete=models.CASCADE,
        related_name='groups'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"
        ordering = ['title']


class Student(models.Model):
    """O'quvchi modeli"""
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    grade = models.IntegerField()

    def __str__(self):
        return f"{self.firstname} {self.lastname or ''}".strip()

    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"
        ordering = ['firstname']