from django.contrib import admin

from apps.core.models import DicoTable, Event, TablePrice, TypeTicket, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "username", "phone_number", "is_active", "created_at"]
    list_filter = ["is_active", "type_user"]
    search_fields = ["email", "username", "phone_number"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "start_time", "end_time", "event_state"]
    list_filter = ["event_state"]
    search_fields = ["name"]


admin.site.register(DicoTable)
admin.site.register(TypeTicket)
admin.site.register(TablePrice)
