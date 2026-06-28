from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import AuditLog, Profile, User

admin.site.register(User, DjangoUserAdmin)
admin.site.register(Profile)
admin.site.register(AuditLog)
