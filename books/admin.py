from django.contrib import admin
from .models import Book, Chapter, Success


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "chapters_count")


class ChapterAdmin(admin.ModelAdmin):
    list_display = ("book", "number")


class SuccessAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "chapter",)


admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Success, SuccessAdmin)
