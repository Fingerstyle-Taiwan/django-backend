from django.urls import path
from contest import views

app_name = 'contest'

urlpatterns = [
    path('', views.ContestView.as_view(), name='contest-list'),
    path('<int:pk>/', views.ContestDetailView.as_view(), name='contest-detail'),
    path('<int:pk>/like/', views.ContestLikeView.as_view(), name='contest-like'),
]
