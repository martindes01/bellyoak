from django import forms

from bellyoak.models import Ingredient, Instruction, Recipe, UserProfile


# Model forms

# labels = {'': "",}
# help_texts = {'': "",}
# error_messages = {'': {'': "",},}

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = (
            'name',
            'quantity',
            'unit',
        )
        widgets={
            'name': forms.TextInput(
                attrs={
                    'required': True,
                }
            ),
            'quantity': forms.NumberInput(
                attrs={
                    'min': 0,
                    'max': 9999999.99,
                    'step': 0.01,
                }
            )
        }

class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = (
            'text',
        )
        widgets={
            'text': forms.Textarea(
                attrs={
                    'required': True,
                }
            )
        }

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title',
            'description',
            'servings',
            'diet',
        )
        widgets = {
            'servings': forms.NumberInput(
                attrs={
                    'min': 1,
                }
            )
        }
        help_texts = {
            'description': "(Optional) Let us know why you love this recipe, what goes well with it or even tell us a funny anecdote. But keep it short, we're starving!",
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'picture',
            'status',
            'website',
            'about_me',
        )
        help_texts = {
            'about_me': "(Optional) Tell others a bit about yourself.",
        }

# Model formsets

IngredientFormSet = forms.modelformset_factory(Ingredient, form=IngredientForm, can_delete=True, min_num=2)

InstructionFormSet = forms.modelformset_factory(Instruction, form=InstructionForm, can_delete=True, min_num=1)
