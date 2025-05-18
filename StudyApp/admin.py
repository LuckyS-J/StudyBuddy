from django.contrib import admin
from . models import User, Goal, Task, Note

# Register your models here.

admin.site.register(Goal)
admin.site.register(Task)
admin.site.register(Note)