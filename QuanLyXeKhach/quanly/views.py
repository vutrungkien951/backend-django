from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, generics, permissions, status

from .perms import CommentOwnerPermisson, UserPermisson, RolePermisson
from .models import User, TuyenXe, ChuyenXe, DatVe, Comment, Like, Rating
from .serializers import (UserSerializer,
                        TuyenXeSerializer,
                        ChuyenXeSerializer,
                        DatVeSerializer,
                        CreateCommentSerializer,
                        CommentSerializer,
                        AuthChuyenXeSerializer,
                        ChuyenXeIdSerializer)
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.
def index(request):
    return HttpResponse("Hello word")


class UserViewSet(viewsets.ViewSet ,generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current-user", detail=False)
    def current_user(self, request):
        return Response(self.serializer_class(request.user, context={'request': request}).data,
                        status=status.HTTP_200_OK)


# admin only
class TuyenXeViewset(viewsets.ViewSet,
                     generics.ListAPIView,
                     generics.CreateAPIView,
                     generics.UpdateAPIView,
                     generics.DestroyAPIView,
                     generics.RetrieveAPIView):
    queryset = TuyenXe.objects.filter(active=True)
    serializer_class = TuyenXeSerializer

    def get_queryset(self):
        query = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(ten_tuyen__icontains=kw)

        return query

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        else:
            if self.action in ['create', 'update', 'destroy', 'retrieve']:
                return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]


# admin only
class ChuyenXeViewset(viewsets.ViewSet,
                     generics.ListAPIView,
                     generics.RetrieveAPIView):
    queryset = ChuyenXe.objects.filter(active=True)
    serializer_class = ChuyenXeSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return AuthChuyenXeSerializer
        return ChuyenXeSerializer

    def get_queryset(self):
        query = self.queryset
        kw = self.request.query_params.get('kw')
        tg = self.request.query_params.get('tg')
        # ddiem = self.request.query_params.get('ddiem')
        if kw:
            query = query.filter(ten_chuyenxe__icontains=kw)
        if tg:
            query = query.filter(khoi_hanh__icontains=tg)
        # if ddiem:
        #     tuyenxe = TuyenXe.objects.filter(active=True)
        #     query = query.filter(tuyen_xe__icontains=ddiem)
        return query

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        chuyenxe = self.get_object()
        comments = chuyenxe.comments.select_related('user').filter(active=True)

        return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        chuyenxe = self.get_object()
        user = request.user

        l, _ = Like.objects.get_or_create(chuyenxe=chuyenxe, user=user)
        l.active = not l.active
        try:
            l.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=AuthChuyenXeSerializer(chuyenxe, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='rating', detail=True)
    def rating(self, request, pk):
        chuyenxe = self.get_object()
        user = request.user

        r, _ = Rating.objects.get_or_create(chuyenxe=chuyenxe, user=user)
        r.rate = request.data.get('rate', 0)
        try:
            r.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=AuthChuyenXeSerializer(chuyenxe, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class DatVeViewset  (viewsets.ViewSet,
                    generics.CreateAPIView,
                    generics.RetrieveAPIView):
    queryset = DatVe.objects.filter(active=True)
    serializer_class = DatVeSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        else:
            if self.action in ['retrieve']:
                return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]


# class ThongKeViewSet (viewsets.ViewSet, generics.ListAPIView):
#     queryset = DatVe.objects.filter(active= True)
#     serializer_class = DatVeSerializer
#
#     @action(methods=['get'], url_path='chuyenxe', detail=False)
#     def chuyenxe(self, request):
#         tuyenxe = TuyenXe.objects.filter(active=True)
#         chuyenxe = ChuyenXe.objects.filter(active=True)
#         for t in tuyenxe:
#             chxe = chuyenxe.filter(tuyen_xe_id=t.id)
#         print(chxe)
#         return HttpResponse(ChuyenXeSerializer(chxe, many=True).data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.CreateAPIView,
                     generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CreateCommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [CommentOwnerPermisson()]

        return [permissions.IsAuthenticated()]

