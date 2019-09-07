from django.contrib import admin

from bellyoak.models import Ingredient, Instruction, Recipe

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'name',
        'quantity',
        'unit',
    )

@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'index',
        'text',
    )

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'servings',
        'diet',
        'views',
        'likes',
    )
    prepopulated_fields = {
        'slug': (
            'title',
        ),
    }
