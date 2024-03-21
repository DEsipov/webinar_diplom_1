#!-*-coding:utf-8-*-
from rest_framework import serializers

from recipes.models import Ingredient, RecipeIngredient, Recipe, Tag


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('amount', 'name', 'measurement_unit', 'id')


class RecipeListSerializer(serializers.ModelSerializer):
    """Получение списка рецептов."""

    ingredients = serializers.SerializerMethodField()
    is_favorite = serializers.BooleanField()
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    def get_ingredients(self, obj):
        """Возвращает отдельный сериализатор."""
        return RecipeIngredientSerializer(
            RecipeIngredient.objects.filter(recipe=obj).all(), many=True
        ).data

    class Meta:
        model = Recipe
        fields = ('name', 'ingredients', 'is_favorite', 'text', 'author')


class IngredientCreateInRecipeSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    ingredients = IngredientCreateInRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'ingredients', 'text', )

    def validate_ingredients(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Добавьте хотя бы один ингредиент.")
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        create_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        RecipeIngredient.objects.bulk_create(
            create_ingredients
        )
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()

            create_ingredients = [
                RecipeIngredient(
                    recipe=instance,
                    ingredient=ingredient['ingredient'],
                    amount=ingredient['amount']
                )
                for ingredient in ingredients
            ]
            RecipeIngredient.objects.bulk_create(
                create_ingredients
            )
        return super().update(instance, validated_data)

    def to_representation(self, obj):
        # FIX: данные для редактирования приходят в одном формате, а отдать
        # их надо в другом формате.

        # Т.к. если мы обычный Recipe засунем в этот сериалайзер.
        # RecipeEditSerializer(instance=recipe), то в объявленное нами
        # поле ingredients, попадет recipe.ingredients,
        # а там объекты Ingredient, а у объекта Ingredient нет атрибута
        # ingredient_id, который мы указали, как источник для id
        # в сериалайзере IngredientInRecipeEditSerializer
        # id = serializers.IntegerField(source='ingredient_id')

        # Поэтому убираем проблемное поле. Чтобы не ломать сериализатор.
        self.fields.pop('ingredients')

        # Аналогично и для тэгов.
        # Убираем проблемное, ставим свое поле.
        # self.fields['tags'] = TagSerializer(many=True)

        # Здесь будет уже OrderedDict с данными.
        representation = super().to_representation(obj)

        # В него и впихиваем, как в обычный словарь
        # ингредиенты в нужном нам формате. Подменить так, как с тэгами не
        # прокатит, т.к. мы поле явно объявили в сериализаторе, как атрибут.
        representation['ingredients'] = RecipeIngredientSerializer(
            RecipeIngredient.objects.filter(recipe=obj).all(), many=True
        ).data

        return representation


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'

    # def validate(self, attrs):
    #     ...
