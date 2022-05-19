from django.contrib import admin
from .models import User, TuyenXe, ChuyenXe, DatVe, VaiTro


# Register your models here.
class DatVeInline(admin.TabularInline):
    model = DatVe

class ChuyenXeAdmin(admin.ModelAdmin):
    inlines = [DatVeInline,]



admin.site.register(VaiTro)
admin.site.register(User)
admin.site.register(TuyenXe)
admin.site.register(ChuyenXe, ChuyenXeAdmin)
admin.site.register(DatVe)
