from django.urls import path

from bellyoak import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('recipe/<int:id>/', views.show_recipe, name='show_recipe'),
    path('recipe/<int:id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/new/', views.add_recipe, name='add_recipe'),
    path('recipes/', views.list_recipes, name='list_recipes'),
    path('user/<username>/', views.show_user, name='show_user'),
    path('users/', views.list_users, name='list_users'),
]
