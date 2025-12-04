from django.urls import path
from . import views

urlpatterns = [
    path('activation/', views.activation_view, name='activation'),
    path('book/<int:schedule_id>/', views.book_mentor_view, name='book_mentor'),
    path('check-transaction/<int:transaction_id>/', views.check_transaction_api, name='check_transaction'),
]