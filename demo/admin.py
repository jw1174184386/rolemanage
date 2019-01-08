from django.contrib import admin
from demo.models import *

admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(Permission)
admin.site.register(PermissionAction)
admin.site.register(RolePermissionAction)
admin.site.register(Menu)
admin.site.register(Action)
admin.site.register(Role)
