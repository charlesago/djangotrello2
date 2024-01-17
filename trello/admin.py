from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(WorkspaceType)
admin.site.register(Visibility)
admin.site.register(Card)
admin.site.register(List)
admin.site.register(Board)
admin.site.register(Workspace)