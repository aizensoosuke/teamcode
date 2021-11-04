from django.contrib import admin
from backend.models import Session

# Register your models here.
class SessionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Session, SessionAdmin)
