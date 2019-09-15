from django.http import HttpResponse
from django.shortcuts import redirect, render

from bellyoak.forms import IngredientForm, IngredientFormSet, InstructionForm, InstructionFormSet, RecipeForm
from bellyoak.models import Ingredient, Instruction, Recipe


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

def recipe_add(request):
    recipe = Recipe(title='Untitled recipe')
    recipe.save()
    return redirect('recipe_edit', recipe.id)

def recipe_edit(request, id):
    try:
        # Find recipe with specified id
        recipe = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        # Render error page if no recipe with specified id
        return render(request, 'bellyoak/recipe_none.html', {})

    if request.method == 'POST':
        # Retrieve form data
        recipe_form = RecipeForm(request.POST, instance=recipe, prefix='recipe')
        ingredient_formset = IngredientFormSet(request.POST, queryset=Ingredient.objects.filter(recipe=recipe), prefix='ingredient')
        instruction_formset = InstructionFormSet(request.POST, queryset=Instruction.objects.filter(recipe=recipe), prefix='instruction')
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
    ingredient_formset = IngredientFormSet(queryset=Ingredient.objects.filter(recipe=recipe), prefix='ingredient')
    instruction_formset = InstructionFormSet(queryset=Instruction.objects.filter(recipe=recipe), prefix='instruction')
    context = {
        'recipe': recipe,
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'instruction_formset': instruction_formset,
    }
    return render(request, 'bellyoak/recipe_edit.html', context)

def recipe_show(request, id):
    try:
        # Find recipe with specified id
        recipe = Recipe.objects.get(id=id)

        context = {
            'recipe': recipe,
            'ingredients': Ingredient.objects.filter(recipe=recipe).order_by('id'),
            'instructions': Instruction.objects.filter(recipe=recipe).order_by('id'),
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

def user_show(request, username):
    context = {}
    return render(request, 'bellyoak/user_show.html', context)

def users_list(request):
    context = {}
    return render(request, 'bellyoak/users_list.html', context)
