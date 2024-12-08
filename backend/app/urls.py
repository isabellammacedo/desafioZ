from django.contrib import admin
from django.urls import path, include
from .views import CompanyViewSet, DocumentViewSet, SignersViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Company', CompanyViewSet)
router.register(r'Document', DocumentViewSet)
router.register(r'Signers', SignersViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
