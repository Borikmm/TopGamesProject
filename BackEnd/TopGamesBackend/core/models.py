from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    # Добавляем related_name, чтобы избежать конфликтов
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Измененное имя реверсной связи
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",  # Измененное имя реверсной связи
        blank=True,
        help_text="Specific permissions for this user.",
    )

# Дисциплины
class Discipline(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Преподаватели
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    disciplines = models.ManyToManyField(Discipline)

    def __str__(self):
        return self.user.username

# Ученики
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    average_rating = models.FloatField(default=0.0)
    disciplines = models.ManyToManyField(Discipline)  # Связь с дисциплинами
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    def __str__(self):
        return self.user.username

# Игры
class Game(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='games')
    name = models.CharField(max_length=255)
    image_url = models.URLField(blank=True, null=True)
    file_path = models.CharField(max_length=255, default="NonePath")

    def __str__(self):
        return self.name

# Оценки
class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.FloatField()

# Прогресс
class Progress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    progress_percentage = models.FloatField()
