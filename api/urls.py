from rest_framework import routers
from django.urls import path, include
from .views import CompanyViewSet, TechnicalViewSet, GenerateOrdersAPIView

router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'technical', TechnicalViewSet, basename='technical')


urlpatterns = [
    path('', include(router.urls)),
    path('generate-orders/', GenerateOrdersAPIView.as_view(), name='generate-orders')
]
