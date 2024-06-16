from django.db import models

from books.models import Book


class Stat(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    books = models.ManyToManyField(Book, related_name="available_stats")

    def __str__(self):
        return f"{self.name}"


class BillyClass(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name="available_classes")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Billy classes"


class ItemTypes(models.TextChoices):
    WEAPON = "WEAPON", "Arme"
    EQUIPMENT = "EQUIPMENT", "Équipement"
    TOOLS = "TOOLS", "Outils"
    OTHER = "OTHER", "Autre"


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=100, choices=ItemTypes.choices)
    books = models.ManyToManyField(Book, related_name="available_items")
    effects = models.ManyToManyField(
        Stat, through="ItemEffect", related_name="affected_stats"
    )
    created_by = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_items",
    )

    # Backward relationships
    billys: "Billy"
    items_effects: "ItemEffect"

    def __str__(self):
        return f"{self.name}"


class ItemEffect(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="item_effects"
    )
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE, null=True, blank=True)
    value = models.IntegerField(default=0, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.item.name} - {self.stat.name}"


class Billy(models.Model):
    name = models.CharField(max_length=100, blank=True, default="Billy")
    billy_class = models.ForeignKey(
        BillyClass, on_delete=models.CASCADE, related_name="billys"
    )
    items = models.ManyToManyField(Item, related_name="billys", blank=True)
    stats = models.ManyToManyField(Stat, through="BillyStat")

    # Backward relationships
    adventure: "Adventure"

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            Adventure.objects.create(billy=self, book=self.billy_class.books.first())
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.adventure.book.title} - {self.billy_class.name}"


class BillyStat(models.Model):
    billy = models.ForeignKey(Billy, on_delete=models.CASCADE)
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0)

    def compute_value(self, action: str, pk: str):
        """Compute the value of the stat based on the items equipped by the Billy.

        Called by the signal update_billystat in billy.signals.py.
        """
        item_effects = ItemEffect.objects.filter(item=pk, stat=self.stat)
        value = self.value
        for effect in item_effects:
            if action == "add":
                value += effect.value
            elif action == "remove":
                value -= effect.value
        self.value = value

    def __str__(self):
        return f"{self.billy.name} - {self.stat.name}"


class AdventureChapter(models.Model):
    adventure = models.ForeignKey(
        "Adventure", on_delete=models.CASCADE, related_name="chapters"
    )
    chapter = models.ForeignKey(
        "books.Chapter", on_delete=models.CASCADE, related_name="adventure_chapters"
    )
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adventure.billy.name} - {self.chapter.number}"


class Adventure(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="adventures")
    billy = models.OneToOneField(
        Billy, on_delete=models.CASCADE, related_name="adventure"
    )
    visited_chapters = models.ManyToManyField(
        "books.Chapter",
        related_name="adventures",
        blank=True,
        through=AdventureChapter,
    )
    successes = models.ManyToManyField(
        "books.Success", related_name="adventures", blank=True
    )

    @property
    def current_chapter(self):
        return self.visited_chapters.last("visited_at")

    def __str__(self):
        return f"{self.billy.name} - {self.book.title}"
