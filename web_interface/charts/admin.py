from django.contrib import admin
from models import Host, FSUsageSample, MemUsageSample

# Register your models here.
admin.site.register(Host)
admin.site.register(FSUsageSample)
admin.site.register(MemUsageSample)
