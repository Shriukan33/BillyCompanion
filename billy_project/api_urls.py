from django.urls import include, path
from rest_framework.routers import DefaultRouter

from billy.urls import router as billy_router
from books.urls import router as books_router

router = DefaultRouter()
router.registry.extend(billy_router.registry)
router.registry.extend(books_router.registry)

urlpatterns = [
    path("", include(router.urls)),
]
