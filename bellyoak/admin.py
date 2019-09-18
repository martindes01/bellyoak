from django.contrib import admin

from bellyoak.models import Ingredient, Instruction, Recipe, UserProfile

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

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'status',
        'website',
        'about_me',
    )
