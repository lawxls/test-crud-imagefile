from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('images', views.ImageViewSet)
router.register('comments', views.CommentViewSet)
router.register('stat', views.StatViewSet, basename='stat')

app_name = 'imagesAPI'

urlpatterns = [
    path('', include(router.urls))
]
