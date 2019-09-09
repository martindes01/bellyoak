import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bellyoak_project.settings')

import django
django.setup()

from bellyoak.models import Ingredient, Instruction, Recipe

from decimal import Decimal


# Keys

TITLE = 'title'
DESCRIPTION = 'description'
SERVINGS = 'servings'
DIET = 'diet'
LIKES = 'likes'
VIEWS = 'views'
INGREDIENTS = 'ingredients'
INSTRUCTIONS = 'instructions'

NAME = 'name'
QUANTITY = 'quantity'
UNIT = 'unit'

TEXT = 'text'


# Functions

# Populate database with test data
def populate():
    # Create lists of ingredients and instructions

    haggis_ingredients = [
        {
            NAME: 'Dehydrated haggis',
            QUANTITY: 123.45,
            UNIT: Ingredient.Unit.KILOGRAM,
        },
        {
            NAME: 'Water',
            QUANTITY: 9000,
            UNIT: Ingredient.Unit.LITRE,
        },
    ]
    haggis_instructions = [
        {
            TEXT: 'Marvel at the dehydrated haggis.',
        },
        {
            TEXT: 'Add the water.',
        },
        {
            TEXT: 'Enjoy.',
        },
    ]

    mars_ingredients = [
        {
            NAME: 'Solid fat',
            QUANTITY: 3000000,
            UNIT: Ingredient.Unit.KILOGRAM,
        },
        {
            NAME: 'Crude oil',
            QUANTITY: 1200,
            UNIT: Ingredient.Unit.PINT,
        },
    ]
    mars_instructions = [
        {
            TEXT: 'Fry! Fry! Fry!',
        },
        {
            TEXT: 'Burn! Burn! Burn!',
        },
        {
            TEXT: 'Die! Die! Die!',
        },
    ]

    nothing_ingredients = [
        {
            NAME: 'Nitrogen',
            QUANTITY: 79,
            UNIT: Ingredient.Unit.TEASPOON,
        },
        {
            NAME: 'Oxygen',
            QUANTITY: 21,
            UNIT: Ingredient.Unit.TEASPOON,
        },
        {
            NAME: 'Grave',
            QUANTITY: 5000,
            UNIT: Ingredient.Unit.NONE,
        },
    ]
    nothing_instructions = [
        {
            TEXT: 'Inhale.',
        },
        {
            TEXT: 'Exhale.',
        },
        {
            TEXT: 'Slowly rot.',
        },
    ]

    # Creat list of recipes, including ingredients and instructions
    recipes = [
        {
            TITLE: 'Yummy haggis',
            DESCRIPTION: 'My old dying relative used to make this for me all the time...',
            SERVINGS: 6,
            DIET: Recipe.Diet.NONE,
            LIKES: 32,
            VIEWS: 64,
            INGREDIENTS: haggis_ingredients,
            INSTRUCTIONS: haggis_instructions,
        },
        {
            TITLE: 'Glasgow\'s finest fried mars bars!',
            DESCRIPTION: 'Feel the fat flow through your veins... ooh yass',
            SERVINGS: 300,
            DIET: Recipe.Diet.VEGETARIAN,
            LIKES: 128,
            VIEWS: 128,
            INGREDIENTS: mars_ingredients,
            INSTRUCTIONS: mars_instructions,
        },
        {
            TITLE: 'F##k all',
            DESCRIPTION: 'Starve to death due to your own incompetence, init',
            SERVINGS: 5000,
            DIET: Recipe.Diet.VEGAN,
            LIKES: 1,
            VIEWS: 1024,
            INGREDIENTS: nothing_ingredients,
            INSTRUCTIONS: nothing_instructions,
        },
    ]

    # Add each recipe
    for data in recipes:
        recipe = add_recipe(data[TITLE], data[DESCRIPTION], data[SERVINGS], data[DIET], data[LIKES], data[VIEWS])

        # Add recipe ingredients
        for ingredient in data[INGREDIENTS]:
            add_ingredient(recipe, ingredient[NAME], ingredient[QUANTITY], ingredient[UNIT])

        # Add recipe instructions
        for instruction in data[INSTRUCTIONS]:
            add_instruction(recipe, instruction[TEXT])

    # Print all recipes
    for recipe in Recipe.objects.all():
        print("\n{0} - {1}".format(recipe.title, recipe.description))
        print("- Servings: {0}, Diet: {1}, Views: {2}, Likes: {3}".format(recipe.servings, recipe.diet, recipe.views, recipe.likes))
        print("- Ingredients:")
        for ingredient in Ingredient.objects.filter(recipe=recipe):
            print("  - {0}, {1} {2}".format(ingredient.name, ingredient.quantity, ingredient.get_unit_display()))
        print("- Instructions:")
        for (index, instruction) in enumerate(Instruction.objects.filter(recipe=recipe), start=1):
            print("  - {0}. {1}".format(index, instruction.text))

# Add ingredient to database
def add_ingredient(recipe, name, quantity=0, unit=Ingredient.Unit.NONE):
    ingredient = Ingredient.objects.get_or_create(recipe=recipe, name=name)[0]
    ingredient.quantity = Decimal(quantity)
    ingredient.unit = unit
    ingredient.save()
    return ingredient

# Add instruction to database
def add_instruction(recipe, text):
    instruction = Instruction.objects.get_or_create(recipe=recipe, text=text)[0]
    instruction.save()
    return instruction

# Add recipe to database
def add_recipe(title, description, servings=1, diet=Recipe.Diet.NONE, likes=0, views=0):
    recipe = Recipe.objects.get_or_create(title=title)[0]
    recipe.description = description
    recipe.servings = servings
    recipe.diet = diet
    recipe.likes = likes
    recipe.views = views
    recipe.save()
    return recipe

# Start execution
if __name__ == '__main__':
    print("Starting BellyOak population script...")
    populate()
