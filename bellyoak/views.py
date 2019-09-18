from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from bellyoak.forms import IngredientForm, IngredientFormSet, InstructionForm, InstructionFormSet, RecipeForm, UserProfileForm
from bellyoak.models import Ingredient, Instruction, Recipe, UserProfile


# TODO
# Decide how to filter and order recipes and users


# Views

def index(request):
    context = {
        'recipes': Recipe.objects.order_by('-likes')[:5],
    }
    return render(request, 'bellyoak/index.html', context)

def about(request):
    context = {}
    return render(request, 'bellyoak/about.html', context)

@login_required
def recipe_add(request):
    recipe = Recipe(title='Untitled recipe')
    recipe.save()
    return redirect('recipe_edit', recipe.id, recipe.slug)

@login_required
def recipe_edit(request, id, recipe_slug=''):
    try:
        # Find recipe with specified id
        recipe = Recipe.objects.get(id=id)

        # Ensure recipe slug visible in url
        if recipe_slug != recipe.slug:
            return redirect('recipe_edit', id, recipe.slug)
    except Recipe.DoesNotExist:
        # Render error page if no recipe with specified id
        return render(request, 'bellyoak/recipe_none.html', {})

    if request.method == 'POST':
        # Retrieve form data
        recipe_form = RecipeForm(request.POST, instance=recipe, prefix='recipe')
        ingredient_formset = IngredientFormSet(request.POST, queryset=recipe.ingredients.all(), prefix='ingredient')
        instruction_formset = InstructionFormSet(request.POST, queryset=recipe.instructions.all(), prefix='instruction')

        if recipe_form.is_valid() and ingredient_formset.is_valid() and instruction_formset.is_valid():
            recipe = recipe_form.save(commit=True)

            # Save ingredient formset but do not commit
            ingredients = ingredient_formset.save(commit=False)
            # Save each ingredient with recipe foreign key
            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()
            # Delete marked ingredients
            for obj in ingredient_formset.deleted_objects:
                obj.delete()

            # Save instruction formset but do not commit
            instructions = instruction_formset.save(commit=False)
            # Save each instruction with recipe foreign key
            for instruction in instructions:
                instruction.recipe = recipe
                instruction.save()
            # Delete marked instructions
            for obj in instruction_formset.deleted_objects:
                obj.delete()

            # Redirect to show recipe
            return redirect('recipe_show', recipe.id)
        else:
            print("recipe " + str(recipe_form.errors))
            print("ingredients " + str(ingredient_formset.errors))
            print("instructions " + str(instruction_formset.errors))

    # If valid GET or invalid POST
    # Render populated form or form with errors
    recipe_form = RecipeForm(instance=recipe, prefix='recipe')
    ingredient_formset = IngredientFormSet(queryset=recipe.ingredients.all(), prefix='ingredient')
    instruction_formset = InstructionFormSet(queryset=recipe.instructions.all(), prefix='instruction')
    context = {
        'recipe': recipe,
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'instruction_formset': instruction_formset,
    }
    return render(request, 'bellyoak/recipe_edit.html', context)

def recipe_show(request, id, recipe_slug=''):
    try:
        # Find recipe with specified id
        recipe = Recipe.objects.get(id=id)

        # Ensure recipe slug visible in url
        if recipe_slug != recipe.slug:
            return redirect('recipe_show', id, recipe.slug)

        context = {
            'recipe': recipe,
            'ingredients': recipe.ingredients.order_by('id'),
            'instructions': recipe.instructions.order_by('id'),
        }
        return render(request, 'bellyoak/recipe_show.html', context)
    except Recipe.DoesNotExist:
        # Render error page if no recipe with specified id
        return render(request, 'bellyoak/recipe_none.html', {})

def recipes_list(request):
    context = {
        'recipes': Recipe.objects.all(),
    }
    return render(request, 'bellyoak/recipes_list.html', context)

@login_required
def user_edit(request):
    # Get user profile or create if does not exist
    profile = UserProfile.objects.get_or_create(user=request.user)[0]

    if request.method == 'POST':
        # Retrieve form data
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile, prefix='profile')

        if profile_form.is_valid():
            # Save profile
            profile = profile_form.save(commit=True)

            # Redirect to home
            return redirect('index')
        else:
            print(profile_form.errors)

    # If valid get or invalid post
    # Render populated form or form with errors
    profile_form = UserProfileForm(instance=profile, prefix='profile')
    context = {
        'profile_form': profile_form,
    }
    return render(request, 'bellyoak/user_edit.html', context)

def user_show(request, username):
    try:
        # Find user with specified username
        user = User.objects.get(username=username)

        # Get user profile or create if does not exist
        profile = UserProfile.objects.get_or_create(user=user)[0]

        context = {
            'owner': username == request.user.username,
            'profile': profile,
        }
        return render(request, 'bellyoak/user_show.html', context)
    except User.DoesNotExist:
        # Render error page if no user with specified username
        context = {
            'username': username,
        }
        return render(request, 'bellyoak/user_none.html', context)

def users_list(request):
    context = {
        'profiles': UserProfile.objects.all(),
    }
    return render(request, 'bellyoak/users_list.html', context)
