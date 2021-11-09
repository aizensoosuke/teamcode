from django.contrib import admin
from backend.models import Session, User

# Register your models here.
class SessionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Session, SessionAdmin)

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)
