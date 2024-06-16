from rest_framework import serializers
from .models import Billy, Adventure, Book, Item, ItemEffect, Stat


class BillySerializer(serializers.ModelSerializer):
    class Meta:
        model = Billy
        fields = (
            "id",
            "name",
            "billy_class",
            "items",
            "stats",
        )

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "chapters_count",
        )
        
class ItemEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemEffect
        fields = (
            "id",
            "item",
            "stat",
            "value",
            "description",
        )

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = (
            "id",
            "name",
            "description",
        )

class ItemSerializer(serializers.ModelSerializer):
    
    effects = ItemEffectSerializer(many=True)

    class Meta:
        model = Item
        fields = (
            "id",
            "name",
            "description",
            "type",
            "books",
            "effects",
            "created_by",
        )

class AdventureSerializer(serializers.ModelSerializer):    
    billy = BillySerializer()
    current_chapter = serializers.ReadOnlyField()

    class Meta:
        model = Adventure
        fields = (
            "id",
            "book",
            "billy",
            "visited_chapters",
            "successes",
            "current_chapter",
        )