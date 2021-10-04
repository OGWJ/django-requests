from django.urls import path
from sentiment_extraction_app import views

urlpatterns = [
    path('queries/', views.query_record_list),
    path('records/<query>/', views.query_record_detail),
]
