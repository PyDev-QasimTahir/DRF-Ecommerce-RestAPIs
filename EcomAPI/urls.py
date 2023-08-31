from django.contrib import admin
from django.urls import path
from EcomAPP import views
from EcomAPP.views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"Product", ProductListCreateAPIView)
router.register(r"Company", CompanyListCreateAPIView)
router.register(r"ShipInfo", ShipInfoListCreateAPIView)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Signup, Login, Logout APIs
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    # Category API
    path('category/', views.CategoryShowAdd.as_view()),
    path('category/<int:pk>/', views.CategoryDeleteUpdateRetrieve.as_view()),
    # Company API
    path('company/', CompanyListCreateAPIView.as_view()),
    path('company/<int:pk>/', CompanyRetrieveUpdateDeleteView.as_view()),
    # Product API
    path('product/', ProductListCreateAPIView.as_view()),
    path('product/<int:pk>/', ProductRetrieveUpdateDeleteView.as_view()),
    # Add-to-Cart API
    path('addcart/', AddToCartView.as_view(), name='add-to-cart'),
    # Shipping Information
    path('shipinfo/', views.ShipInfoListCreateAPIView.as_view()),
    path('shipinfo/<int:pk>/', views.ShipInfoRetrieveUpdateDeleteView.as_view()),
    # Payment Method:
    path('payment/', CreatePaymentMethodView.as_view(), name='create-payment'),
]