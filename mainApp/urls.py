from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import UserViewSet, UserProfileViewSet, ProductsViewSet, SuppliersViewSet, OrdersViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('userProfile', UserProfileViewSet)
router.register('Products', ProductsViewSet)
router.register('Suppliers', SuppliersViewSet)
router.register('Orders', OrdersViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
