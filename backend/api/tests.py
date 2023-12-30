#!-*-coding:utf-8-*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITransactionTestCase
from rest_framework.authtoken.models import Token

from recipes.models import User, Recipe, Ingredient, RecipeIngredient, Tag


class RecipesApiTestCase(APITransactionTestCase):
    """Тесты api рецептов."""

    @classmethod
    def setUpClass(cls):
        cls.url = reverse('recipe-list')

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='vi')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.recipe = Recipe.objects.create(
            author=self.user,
            name='Cookie',
            text='Badabada',
        )
        self.salt = Ingredient.objects.create(
            name='Salt',
            measurement_unit='kg',
        )
        self.recipe_ing = RecipeIngredient.objects.create(
            ingredient=self.salt,
            amount=32,
            recipe=self.recipe
        )

    def test_list(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        obj = resp.data[0]
        self.assertEqual(obj['name'], self.recipe.name)
        ing = obj['ingredients'][0]
        self.assertEqual(ing.get('id'), self.salt.id)
        self.assertEqual(ing.get('amount'), self.recipe_ing.amount)
        self.assertEqual(ing.get('name'), self.salt.name)

    def test_create_recipe(self):
        data = dict(
            name='Pie',
            text='Create pie',
            ingredients=[{'id': self.salt.id, 'amount': '22'}, ]
        )

        resp = self.client.post(self.url, data=data)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        ingredients = data.pop('ingredients')
        self.assertTrue(Recipe.objects.filter(**data).exists())
        ing = ingredients[0]
        self.assertEqual(ing.get('id'), self.salt.id)
        rec_ing = RecipeIngredient.objects.filter(
            amount=ing.get('amount'),
            ingredient=self.salt.id).last()
        self.assertEqual(ing.get('amount'), str(rec_ing.amount))


class TagApiTestCase(APITransactionTestCase):
    """Тесты api тэгов."""

    def setUp(self) -> None:
        self.tag = Tag.objects.create(
            name='dinner',
            color='black',
            slug='din'
        )

    def test_list(self):
        url = reverse('tags-list')

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        obj = resp.data[0]
        self.assertEqual(obj['name'], self.tag.name)
