from django.contrib import admin

from tekis.board import models


class BoardMemberInline(admin.TabularInline):
    model = models.BoardMember


class BoardAdmin(admin.ModelAdmin):
    inlines = [BoardMemberInline]


admin.site.register(models.Board, BoardAdmin)
