from django.http import HttpResponse
from django.shortcuts import render

from bellyoak.models import Diet, Ingredient, Instruction, Recipe, Unit


# TODO
# Decide how to filter and order recipes and users


# Views

def index(request):
    context_dict = {
        'no_diet': Diet.NONE,
        'no_unit': Unit.NONE,
        'recipes': Recipe.objects.order_by('-likes')[:5],
    }
    return render(request, 'bellyoak/index.html', context_dict)

def about(request):
    context_dict = {}
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
        'no_diet': Diet.NONE,
        'no_unit': Unit.NONE,
        'recipes': Recipe.objects.all(),
    }
    return render(request, 'bellyoak/recipes.html', context_dict)

def list_users(request):
    context_dict = {
        'message': "list_users",
    }
    return render(request, 'bellyoak/users.html', context_dict)

def show_recipe(request, id):
    context_dict = {
        'no_diet': Diet.NONE,
        'no_unit': Unit.NONE,
    }

    try:
        recipe = Recipe.objects.get(id=id)
        context_dict['recipe'] = recipe
        context_dict['ingredients'] = Ingredient.objects.filter(recipe=recipe).order_by('id')
        context_dict['instructions'] = Instruction.objects.filter(recipe=recipe).order_by('id')
    except Recipe.DoesNotExist:
        context_dict['recipe'] = None
        context_dict['ingredients'] = None
        context_dict['instructions'] = None

    return render(request, 'bellyoak/recipe.html', context_dict)

def show_user(request, username):
    context_dict = {
        'title': username,
        'message': "show_user",
    }
    return render(request, 'bellyoak/user.html', context_dict)
