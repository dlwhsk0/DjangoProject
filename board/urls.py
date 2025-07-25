from django.urls import path

from . import views
from .views import LikeViewSet
from rest_framework.routers import DefaultRouter

app_name = 'board' # create 등의 이름이 겹칠 수 있으니까 별칭 지정

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:board_id>/', views.detail, name='detail'),
    path('create/', views.board_create, name='board_create'),
    path('delete/<int:board_id>/', views.board_delete, name='board_delete'),
    path('update/<int:board_id>/', views.board_update, name='board_update'),
]

router = DefaultRouter()
router.register(r'likes', LikeViewSet)