from rest_framework import permissions


class CommentOwnerPermisson(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, comment):
        return request.user == comment.user


class UserPermisson(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class RolePermisson(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        # print('a')
        # print(request.user.vai_tro_id)
        return request.user.vai_tro_id == 1


class CusPermisson(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        # print('a')
        # print(request.user.vai_tro_id)
        return request.user.vai_tro_id == 4
