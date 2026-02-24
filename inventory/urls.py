from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.books_api), 
    
    path('books/<int:book_id>/', views.book_detail_api),
]