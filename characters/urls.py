from django.urls import path

from . import views

urlpatterns = [
    path('', views.CharacterListView.as_view(), name='character-list'),
    path('characters/new/', views.CharacterCreateView.as_view(), name='character-create'),
    path('characters/<int:pk>/', views.CharacterDetailView.as_view(), name='character-detail'),
    path('characters/<int:pk>/edit/', views.CharacterUpdateView.as_view(), name='character-edit'),
    path('characters/<int:pk>/delete/', views.CharacterDeleteView.as_view(), name='character-delete'),
]
