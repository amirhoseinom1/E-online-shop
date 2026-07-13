from django.urls import path
from .import views
from accounts.views import CommentCreateView

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/', views.ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
path('product/<slug:slug>/comment/', CommentCreateView.as_view(), name='comment_create'),
]