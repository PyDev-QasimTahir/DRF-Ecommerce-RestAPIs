from EcomAPP import views
from EcomAPP.views import *
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from dj_rest_auth.views.registration import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

router = DefaultRouter()
router.register(r"Product", ProductListCreateAPIView)
router.register(r"Company", CompanyListCreateAPIView)
router.register(r"ShipInfo", ShipInfoListCreateAPIView)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Social Login
    path('accounts/', include('allauth.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('dj-rest-auth/github/', GithubLogin.as_view(), name='github_login'),
    # path('dj-rest-auth/registration/', RegisterView.as_view(), name='rest_register'),
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