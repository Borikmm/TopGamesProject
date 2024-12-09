from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import *
from .serializers import *
from .permissions import IsAdmin, IsTeacher, IsStudent
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Teacher, User
from .serializers import TeacherSerializer
from django.http import JsonResponse
import os
import zipfile
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Game, Discipline
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_games(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'role': user.role,  # Возвращаем роль
        })


class CurrentStudentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({"detail": "Студент не найден"}, status=404)

        serializer = StudentSerializer(student)
        return Response(serializer.data)

class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer

# # дописать
#     @action(detail=False, methods=['post'])
#     def create_discipline(self, request):
#         # Создание пользователя с ролью "teacher"
#         user_data = request.data.get('discipline')
#         if not user_data:
#             return Response({"error": "Discipline is required"}, status=status.HTTP_400_BAD_REQUEST)
#
#         discipline = Discipline.objects.create()
#         return Response(TeacherSerializer(discipline).data, status=status.HTTP_201_CREATED)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Удаляем связанного пользователя
        instance.user.delete()
        return Response({"detail": "Преподаватель удалён"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def my_disciplines(self, request):
        user = request.user
        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            return Response({"detail": "Преподаватель не найден"}, status=404)

        disciplines = teacher.disciplines.all()
        data = [{"id": d.id, "name": d.name} for d in disciplines]
        return Response(data)

    @action(detail=False, methods=['post'])
    def create_teacher(self, request):
        # Создание пользователя с ролью "teacher"
        user_data = request.data.get('user')
        if not user_data:
            return Response({"error": "User data is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password'],
            role='teacher'
        )
        teacher = Teacher.objects.create(user=user)
        return Response(TeacherSerializer(teacher).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def update_disciplines(self, request, pk=None):
        teacher = self.get_object()
        discipline_ids = request.data.get('discipline_ids', [])
        teacher.disciplines.set(discipline_ids)  # Обновляем дисциплины
        teacher.save()
        return Response(TeacherSerializer(teacher).data)

    @action(detail=False, methods=['get'])
    def my_students(self, request):
        """
        Возвращаем студентов текущего преподавателя.
        """
        user = request.user
        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            return Response({"detail": "Преподаватель не найден"}, status=404)

        students = teacher.students.all()  # Студенты, связанные с преподавателем
        return Response(StudentSerializer(students, many=True).data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def current_teacher(self, request):
        """
        Возвращает данные текущего преподавателя.
        """
        try:
            teacher = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            return Response({"detail": "Преподаватель не найден"}, status=404)

        data = {
            "id": teacher.id,
            "username": teacher.user.username,
            "disciplines": [{"id": d.id, "name": d.name} for d in teacher.disciplines.all()],
        }
        return Response(data)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Удаляем связанного пользователя
        instance.user.delete()
        return Response({"detail": "Студент удалён"}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        """
        Фильтруем студентов, чтобы преподаватель видел только своих.
        """
        user = self.request.user
        if hasattr(user, 'teacher'):
            return Student.objects.filter(teacher=user.teacher)  # Студенты текущего преподавателя
        return Student.objects.all()  # Администратор видит всех


    @action(detail=False, methods=['post'])
    def create_student(self, request):
        # Создание пользователя с ролью "student"
        user_data = request.data.get('user')
        teacher_id = request.data.get('teacher_id')  # ID преподавателя
        print(teacher_id)

        if not user_data or not teacher_id:
            return Response({"error": "User data is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Проверяем существование преподавателя
        teacher = get_object_or_404(Teacher, id=teacher_id)

        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password'],
            role='student'
        )
        student = Student.objects.create(user=user, teacher=teacher)
        return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def disciplines_and_games(self, request, pk=None):
        student = self.get_object()
        disciplines = student.disciplines.all()
        data = [
            {
                'id': d.id,
                'name': d.name,
                'games': [{'id': g.id, 'name': g.name} for g in d.game_set.all()],
            }
            for d in disciplines
        ]
        return Response(data)

    @action(detail=True, methods=['post'])
    def update_disciplines(self, request, pk=None):
        student = self.get_object()
        discipline_ids = request.data.get('discipline_ids', [])
        print(discipline_ids)
        student.disciplines.set(discipline_ids)  # Обновляем дисциплины
        student.save()
        return Response(StudentSerializer(student).data)

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer



import shutil

class GameDeleteView(APIView):
    def delete(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({"error": "Игра не найдена"}, status=status.HTTP_404_NOT_FOUND)


        # Удаляем картинку
        if game.image_url:
            shutil.rmtree(game.image_url, ignore_errors=True)

        # Удаляем файлы игры из файловой системы
        if game.file_path:
            shutil.rmtree(game.file_path, ignore_errors=True)



        # Удаляем запись из базы данных
        game.delete()

        return Response({"message": "Игра успешно удалена"}, status=status.HTTP_204_NO_CONTENT)


class AddGameView(APIView):
    def post(self, request):
        name = request.data.get('name')  # Имя игры
        discipline_id = request.data.get('discipline_id')  # ID дисциплины
        file = request.FILES.get('file')  # Загруженный ZIP файл
        image = request.FILES.get('image')  # Загруженный iamge

        print(file)
        print(image)


        if not name or not discipline_id or not file or not image:
            return Response({"error": "Все поля обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем существование дисциплины
        try:
            discipline = Discipline.objects.get(id=discipline_id)
        except Discipline.DoesNotExist:
            return Response({"error": "Дисциплина не найдена"}, status=status.HTTP_404_NOT_FOUND)

        # Пути для игры
        unity_games_path = os.path.join(settings.STATICFILES_DIRS[0], 'unity-games')

        # Путь для картинок
        images_path = os.path.join(settings.STATICFILES_DIRS[0], 'games-images')

        target_path = os.path.join(unity_games_path, name)


        os.makedirs(unity_games_path, exist_ok=True)

        # Временный путь для сохранения ZIP файла
        zip_file_path = os.path.join(unity_games_path, file.name)

        # Сохраняем загруженный ZIP файл
        with open(zip_file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Сохраняем картинку
        image_filename = f"{name}.png"  # Например, сохраняем с именем игры
        image_path = os.path.join(images_path, image_filename)
        with open(image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        try:
            # Распаковываем архив
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                # Извлекаем содержимое архива во временную папку
                temp_extract_path = os.path.join(unity_games_path, f"temp_{name}")
                zip_ref.extractall(temp_extract_path)

                # Проверяем содержимое распакованной папки
                extracted_items = os.listdir(temp_extract_path)
                if len(extracted_items) != 1:
                    return Response({"error": "Архив должен содержать одну корневую папку"}, status=status.HTTP_400_BAD_REQUEST)

                # Единственная папка в архиве
                extracted_folder = extracted_items[0]
                extracted_folder_path = os.path.join(temp_extract_path, extracted_folder)

                # Переименовываем распакованную папку в имя игры
                os.rename(extracted_folder_path, target_path)

                # Удаляем временную папку
                os.rmdir(temp_extract_path)
        except zipfile.BadZipFile:
            return Response({"error": "Неправильный архив"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Удаляем ZIP файл
            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)

        # Сохраняем информацию об игре в базе данных
        game = Game.objects.create(name=name, discipline=discipline, file_path=target_path, image_url=f"/static/games-images/{image_filename}")
        return Response(
            {"id": game.id, "name": game.name, "discipline_name": discipline.name},
            status=status.HTTP_201_CREATED
        )