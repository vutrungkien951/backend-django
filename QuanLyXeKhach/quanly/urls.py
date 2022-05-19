from django.urls import path, include
from . import views
from rest_framework import routers


route = routers.DefaultRouter()
route.register("user", views.UserViewSet, basename='user')
route.register("tuyenxe", views.TuyenXeViewset, basename='tuyenxe')
route.register("chuyenxe", views.ChuyenXeViewset, basename='chuyenxe')
route.register("datve", views.DatVeViewset, basename='datve')
route.register(prefix='comments', viewset=views.CommentViewSet, basename='comment')

urlpatterns = [
    path('index/', views.index),
    path('', include(route.urls)),
]
