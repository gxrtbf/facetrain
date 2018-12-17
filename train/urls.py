from django.urls import path

from train import views

urlpatterns = [
    path('login/', views.login_view),
    path('register/', views.register_view),
    path('upload/', views.upload_view),
    path('api/v1/imagelogin/', views.ImageLoginApi.as_view()),
    path('api/v1/uploadface/', views.UploadRecordAPI.as_view()),
    path('api/v1/addvector/', views.AddVertorAPI.as_view()),
]