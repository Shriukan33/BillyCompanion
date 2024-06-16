from rest_framework import viewsets

from .models import Book, Chapter, Success
from .serializers import BookSerializer, ChapterSerializer, SuccessSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


class SuccessViewSet(viewsets.ModelViewSet):
    queryset = Success.objects.all()
    serializer_class = SuccessSerializer
