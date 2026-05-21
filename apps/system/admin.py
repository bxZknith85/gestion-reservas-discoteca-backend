from django.contrib import admin

from apps.system.models import AdminActionLog, AppConfig

admin.site.register(AdminActionLog)
admin.site.register(AppConfig)
