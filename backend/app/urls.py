from django.contrib import admin
from django.urls import path, include
from .views import CompanyViewSet, DocumentView, DocumentViewSet, SignersViewSet
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'Company', CompanyViewSet)
router.register(r'Document', DocumentViewSet)
router.register(r'Signers', SignersViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="ZapSign",
        default_version='v1',
        description="Documentação"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('api/docs/', DocumentView.as_view()),
    path('api/docs/<int:pk>/', DocumentView.as_view()),
]
