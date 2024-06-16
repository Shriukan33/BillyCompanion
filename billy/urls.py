from rest_framework.routers import DefaultRouter

from .views import (
    AdventureViewSet,
    BillyViewSet,
    BookViewSet,
    ItemEffectViewSet,
    ItemViewSet,
    StatViewSet,
)

router = DefaultRouter()
router.register(r"billy", BillyViewSet)
router.register(r"book", BookViewSet)
router.register(r"item", ItemViewSet)
router.register(r"adventure", AdventureViewSet)
router.register(r"item_effect", ItemEffectViewSet)
router.register(r"stat", StatViewSet)
