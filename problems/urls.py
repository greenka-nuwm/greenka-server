from django.urls import path, include
from problems import views


states = [
    path('', views.ProblemStateView.as_view()),
    path('<int:pk>/', views.ProblemStateRUDView.as_view())
]

types = [
    path('', views.ProblemTypeView.as_view()),
    path('<int:pk>/', views.ProblemTypeRUDView.as_view())
]

urlpatterns = [
    path('', views.ProblemView.as_view()),
    path('<int:pk>/', views.ProblemRUDView.as_view()),
    path('types/', include(types)),
    path('states/', include(states)),
]