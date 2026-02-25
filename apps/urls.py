from django.urls import path
from .views import (
    home_page, 
    blog_list, 
    blog_detail, 
    categories_page, 
    category_detail, 
    contact_page,
    profile,
    blog_edit,
    blog_delete,
    blog_like,
    register,
    login_view,
    logout_view
)
from apps import views

urlpatterns = [
    path('', home_page, name='home'),
    path('blog/', blog_list, name='blog_list'),
    path('blog/<int:pk>/', blog_detail, name='blog_detail'),
    path('blog/<int:pk>/like/', blog_like, name='blog_like'),
    path('categories/', categories_page, name='categories'),
    path('category/<int:pk>/', category_detail, name='category_detail'),
    path('contact/', contact_page, name='contact'),
    path('profile/', profile, name='profile'),
    path('profile/blog/<int:pk>/edit/', blog_edit, name='blog_edit'),
    path('profile/blog/<int:pk>/delete/', blog_delete, name='blog_delete'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
