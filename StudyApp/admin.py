from django.contrib import admin
from . models import Users, Goals, Tasks, Notes

# Register your models here.

admin.site.register(Users)
admin.site.register(Goals)
admin.site.register(Tasks)
admin.site.register(Notes)