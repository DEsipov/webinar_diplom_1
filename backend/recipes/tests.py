from django.test import TestCase

from recipes.models import Recipe, Ingredient, RecipeIngredient, Favorite
from users.models import User


class RecipeModelTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='vi')
        self.recipe = Recipe.objects.create(author=self.user)
        self.salt = Ingredient.objects.create(
            name='salt', measurement_unit='pood')

    def test_ingredients(self):
        """Тест добавления ингредиентов в рецепт."""
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.salt,
            amount=1)

        ing = self.recipe.ingredients.first()
        self.assertEqual(ing, self.salt)
        self.assertEqual(self.recipe.recipeingredient_set.first().amount,
                         recipe_ingredient.amount)

    def test_favorite_annotations(self):
        Favorite.objects.create(recipe=self.recipe, user=self.user)

        qs = Recipe.objects.add_user_annotations(user_id=self.user.id)
        self.assertEqual(qs.values()[0]['is_favorite'], True)
