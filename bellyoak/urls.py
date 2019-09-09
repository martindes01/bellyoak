from django.urls import path

from bellyoak import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('recipe/<int:id>/', views.recipe_show, name='recipe_show'),
    path('recipe/<int:id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/new/', views.recipe_add, name='recipe_add'),
    path('recipes/', views.recipes_list, name='recipes_list'),
    path('user/<username>/', views.user_show, name='user_show'),
    path('users/', views.users_list, name='users_list'),
]
