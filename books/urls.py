from rest_framework.routers import DefaultRouter

from .views import BookViewSet, ChapterViewSet, SuccessViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"chapters", ChapterViewSet)
router.register(r"successes", SuccessViewSet)
