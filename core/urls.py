from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, UpdateProfileView, DeleteAccountView,
    AdminRulesView, MockProductsView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/delete/', DeleteAccountView.as_view(), name='delete_account'),
    path('admin/rules/', AdminRulesView.as_view(), name='admin_rules_list'),
    path('admin/rules/<int:pk>/', AdminRulesView.as_view(), name='admin_rules_detail'),
    path('products/', MockProductsView.as_view(), name='products'),
]