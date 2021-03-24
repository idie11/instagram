from django.contrib import admin

# Register your models here.
from users.models import User, Favorites

admin.site.register(User)
admin.site.register(Favorites)