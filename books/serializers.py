from rest_framework import serializers

from .models import Book, Chapter, Success


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "chapters_count",
        )


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = (
            "id",
            "book",
            "number",
        )


class SuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Success
        fields = (
            "id",
            "name",
            "description",
            "chapter",
        )
