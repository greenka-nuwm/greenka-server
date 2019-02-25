from django.urls import path
from gauth import views


urlpatterns = [
    path('self/profile/', views.get_self_profile),
    path('self/trees/', views.get_self_trees),
    path('self/problems/', views.get_self_problems),
    path('register/', views.register),
    path('feedback/', views.FeedbackView.as_view()),
    path('feedback/<int:pk>/image/', views.FeedbackImageView.as_view()),
]
