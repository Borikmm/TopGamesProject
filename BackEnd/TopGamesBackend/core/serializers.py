from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Discipline


class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'name']

class CreateTeacherSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)


class TeacherSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    disciplines = DisciplineSerializer(many=True, read_only=True)  # Дисциплины, привязанные к преподавателю
    discipline_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Discipline.objects.all(),
        write_only=True,
        source='disciplines'
    )  # Позволяет передавать список ID дисциплин для связывания

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'user_name', 'disciplines', 'discipline_ids']

class StudentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    disciplines = DisciplineSerializer(many=True, read_only=True)  # Дисциплины, привязанные к преподавателю
    discipline_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Discipline.objects.all(),
        write_only=True,
        source='disciplines'
    )
    games = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'user', 'user_name', 'average_rating', 'disciplines', 'discipline_ids', 'games']

    def get_games(self, obj):
        games = Game.objects.filter(discipline__in=obj.disciplines.all())
        return GameSerializer(games, many=True).data

class GameSerializer(serializers.ModelSerializer):
    discipline_name = serializers.CharField(source='discipline.name', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ['id', 'name', 'discipline_name', 'image_url', 'file_path']

    def get_image_url(self, obj):
        return f"/static/games-images/{obj.name}.png"

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = '__all__'
