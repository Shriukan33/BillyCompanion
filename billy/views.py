from rest_framework import viewsets

from .models import Adventure, Billy, Book, Item, ItemEffect, Stat
from .serializers import (
    AdventureSerializer,
    BillySerializer,
    BookSerializer,
    ItemEffectSerializer,
    ItemSerializer,
    StatSerializer,
)


class BillyViewSet(viewsets.ModelViewSet):
    queryset = Billy.objects.all()
    serializer_class = BillySerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class AdventureViewSet(viewsets.ModelViewSet):
    queryset = Adventure.objects.all()
    serializer_class = AdventureSerializer
    
class ItemEffectViewSet(viewsets.ModelViewSet):
    queryset = ItemEffect.objects.all()
    serializer_class = ItemEffectSerializer
    
class StatViewSet(viewsets.ModelViewSet):
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
