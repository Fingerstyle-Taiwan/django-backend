from django.urls import path
from contest import views

app_name = 'contest'

urlpatterns = [
    path('list/', views.ContestView.as_view(), name='contest-list')
]
