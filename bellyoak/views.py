from django.http import HttpResponse
from django.shortcuts import render

# Views

def index(request):
    context_dict = {
        'message': "index",
    }
    return render(request, 'bellyoak/index.html', context_dict)

def about(request):
    context_dict = {
        'message': "about",
    }
    return render(request, 'bellyoak/about.html', context_dict)

def add_recipe(request):
    context_dict = {
        'title': "New recipe",
        'message': "add_recipe",
    }
    return render(request, 'bellyoak/recipe.html', context_dict)

def edit_recipe(request, id):
    context_dict = {
        'title': "Editing " + str(id),
        'message': "edit_recipe",
    }
    return render(request, 'bellyoak/recipe.html', context_dict)

def list_recipes(request):
    context_dict = {
        'message': "list_recipes",
    }
    return render(request, 'bellyoak/recipes.html', context_dict)

def list_users(request):
    context_dict = {
        'message': "list_users",
    }
    return render(request, 'bellyoak/users.html', context_dict)

def show_recipe(request, id):
    context_dict = {
        'title': str(id),
        'message': "show_recipe",
    }
    return render(request, 'bellyoak/recipe.html', context_dict)

def show_user(request, username):
    context_dict = {
        'title': username,
        'message': "show_user",
    }
    return render(request, 'bellyoak/user.html', context_dict)
