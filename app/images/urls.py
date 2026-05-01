from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_list, name='image_list'),
    path('upload/', views.image_upload, name='image_upload'),
    path('image/<int:pk>/', views.image_detail, name='image_detail'),
    path('health/', views.health, name='health'),
    path('media/<path:path>', views.serve_minio_image, name='serve_minio_image'),
    path('subscribe/', views.subscribe, name='subscribe'),
]
