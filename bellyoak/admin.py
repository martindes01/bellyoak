from django.contrib import admin

from bellyoak.models import Ingredient, Instruction, Recipe

admin.site.register(Ingredient)
admin.site.register(Instruction)
admin.site.register(Recipe)
