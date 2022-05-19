from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class VaiTro(models.Model):
    ten_vt = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.ten_vt


class User(AbstractUser):
    hinh_anh = models.ImageField(null=True, blank=True, upload_to='user/%Y/%m')
    so_dt = models.CharField(max_length=12, null=True, default=1)
    vai_tro = models.ForeignKey(VaiTro, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class TuyenXe(ModelBase):
    ten_tuyen = models.CharField(max_length=200, null=False)
    diem_di = models.CharField(max_length=255, null=False)
    diem_den = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.ten_tuyen


class ChuyenXe(ModelBase):

    def SoLuongVeDaDat(self):
        list = self.ds_dat_ve.all()
        sum = 0
        for item in list:
            sum += item.so_luong_ve
        return sum

    ten_chuyenxe = models.CharField(max_length=255)
    tai_xe = models.ForeignKey(User, on_delete=models.CASCADE)
    khoi_hanh = models.DateTimeField()
    tuyen_xe = models.ForeignKey(TuyenXe, null=True, on_delete=models.CASCADE)
    sl_ghe = models.SmallIntegerField()
    gia_ve = models.BigIntegerField(default=1)
    # tag = models.ManyToManyField('Tag')

    def __str__(self):
        return self.ten_chuyenxe



class DatVe(ModelBase):
    nguoi_dat = models.ForeignKey(User, on_delete=models.CASCADE)
    chuyen_xe = models.ForeignKey(ChuyenXe, on_delete=models.CASCADE, related_name='ds_dat_ve')
    so_luong_ve = models.SmallIntegerField()

    def __str__(self):
        return self.chuyen_xe.ten_chuyenxe


class Comment(ModelBase):
    noi_dung = models.TextField()
    chuyen_xe = models.ForeignKey(ChuyenXe,
                               related_name='comments',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.noi_dung


# class Tag(ModelBase):
#     name = models.CharField(max_length=50, unique=True)
#
#     def __str__(self):
#         return self.name


class ActionBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chuyenxe = models.ForeignKey(ChuyenXe, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'chuyenxe')
        abstract = True


class Like(ActionBase):
    active = models.BooleanField(default=False)


class Rating(ActionBase):
    rate = models.SmallIntegerField(default=0)
