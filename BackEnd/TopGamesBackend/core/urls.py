from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path

router = DefaultRouter()
router.register(r'disciplines', DisciplineViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'students', StudentViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'progress', ProgressViewSet)

urlpatterns = router.urls



urlpatterns += [
    path('current-user/', CurrentUserView.as_view(), name='current-user'),
    path('current-student/', CurrentStudentView.as_view(), name='current-student'),
    path('games/', get_games, name='get-games'),
]

urlpatterns += [
    path('games/add/', AddGameView.as_view(), name='add-game'),
    path('games/<int:pk>/', GameDeleteView.as_view(), name='delete-game'),  # Удаление игры
]

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]