from django.db import models


class BookTitles(models.TextChoices):
    FDCN = "FDCN", "La Forteresse du Chaudron Noir"
    CDSI = "CDSI", "La Corne des Sables d'Ivoire"


class Book(models.Model):
    title = models.CharField(
        max_length=500, choices=BookTitles.choices, default=BookTitles.FDCN
    )
    chapters_count = models.PositiveIntegerField(default=0)

    # Backward relationships
    chapters: "models.QuerySet[Chapter]"
    successes: "models.QuerySet[Success]"

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chapters")
    number = models.PositiveIntegerField()


class Success(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="successes")

    def __str__(self):
        return f"{self.name} - {self.book.title}"
