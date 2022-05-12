from rest_framework.serializers import ModelSerializer
from .models import User, TuyenXe, ChuyenXe, DatVe, Comment, Like, Rating
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(user.password)
        # if user.vai_tro != 4:
        #     pass
        user.save()
        return user

    def update(self, instance, validated_data):
        user = User(**validated_data)
        user.set_password(user.password)
        user.save()
        return user

    hinh_anh = serializers.SerializerMethodField(source='hinh_anh')

    def get_hinh_anh(self, obj):
        request = self.context['request']
        if obj.avatar and not obj.avatar.name.startswith("/static"):
            path = '/static/%s' % obj.avatar.name

            return request.build_absolute_uri(path)

    # lien_ket_anh = serializers.SerializerMethodField(source='hinh_anh')
    #
    # def get_lien_ket_anh(self, obj):
    #     request = self.context['request']
    #     if obj.hinh_anh and not obj.hinh_anh.name.startswith('/static'):
    #         path = '/static/%s' % obj.hinh_anh.name
    #         return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'hinh_anh', 'vai_tro']
        extra_kwargs = {
            'password': {
                'write_only': True
             }
        }


class TuyenXeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuyenXe
        fields = ['id', 'ten_tuyen', 'diem_di', 'diem_den']


class ChuyenXeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChuyenXe
        fields = ['id', 'ten_chuyenxe', 'tai_xe', 'khoi_hanh', 'tuyen_xe', 'sl_ghe', 'gia_ve']


class TaiXeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChuyenXe
        fields = ['id', 'ten_chuyenxe', 'tai_xe']


class DatVeSerializer(ModelSerializer):
    class Meta:
        model = DatVe
        fields = ['id', 'nguoi_dat', 'chuyen_xe', 'so_luong_ve']


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'noi_dung', 'chuyen_xe', 'user']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'noi_dung', 'created_date', 'updated_date', 'user']


class ThongKeSerializer(ModelSerializer):
    class Meta:
        model = DatVe
        fields = ['id', 'nguoi_dat', 'chuyen_xe', 'so_luong_ve', 'tuyenxe', 'created_date']
