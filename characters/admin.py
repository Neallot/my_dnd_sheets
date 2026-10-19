from django.contrib import admin

from .models import Character


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'master', 'level', 'char_class', 'updated_at')
    list_filter = ('level', 'char_class')
    search_fields = ('name', 'owner__username', 'master__username')
