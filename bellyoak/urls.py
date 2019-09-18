from django.urls import path

from bellyoak import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('account/profile/edit/', views.user_edit, name='user_edit'),
    path('recipe/<int:id>/', views.recipe_show, name='recipe_show'),
    path('recipe/<int:id>/<slug:recipe_slug>/', views.recipe_show, name='recipe_show'),
    path('recipe/<int:id>/<slug:recipe_slug>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/new/', views.recipe_add, name='recipe_add'),
    path('recipes/', views.recipes_list, name='recipes_list'),
    path('user/<username>/', views.user_show, name='user_show'),
    path('users/', views.users_list, name='users_list'),
]
