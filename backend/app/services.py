from .repositories import PreferenceRepository, RecipeRepository


class DashboardService:
    def __init__(self, recipe_repository: RecipeRepository):
        self.recipe_repository = recipe_repository

    def get_dashboard(self):
        recipes = self.recipe_repository.list_all()
        featured = recipes[0]
        return {
            "featured_recipe": featured,
            "recommended_recipes": recipes,
            "stats": {
                "calories": "1450 / 2000 kcal",
                "weight": "68.5 kg",
                "savings": "18.40 zł",
            },
        }


class PreferenceService:
    def __init__(self, preference_repository: PreferenceRepository):
        self.preference_repository = preference_repository

    def get_preferences(self):
        return self.preference_repository.get_first()

    def save_preferences(self, payload: dict):
        return self.preference_repository.save(payload)


class RecipeService:
    def __init__(self, recipe_repository: RecipeRepository):
        self.recipe_repository = recipe_repository

    def list_recipes(self):
        return self.recipe_repository.list_all()

    def get_recipe(self, recipe_id: int):
        return self.recipe_repository.get_by_id(recipe_id)


class ShoppingListBuilder:
    def __init__(self, recipe_repository: RecipeRepository):
        self.recipe_repository = recipe_repository

    def build(self, recipe_id: int):
        recipe = self.recipe_repository.get_by_id(recipe_id)
        items = [
            {
                "id": ingredient.id,
                "name": ingredient.name,
                "quantity": ingredient.quantity,
                "store": ingredient.store,
                "price": ingredient.price,
                "note": ingredient.note or "Promocja",
            }
            for ingredient in recipe.ingredients
        ]
        total_price = round(sum(item["price"] for item in items), 2)
        regular_price = round(total_price + 8.99, 2)
        return {
            "store_name": "Biedronka",
            "address": "ul. Przykładowa 15, Gdańsk",
            "distance": "850 m",
            "walking_time": "8 min pieszo",
            "total_price": total_price,
            "regular_price": regular_price,
            "savings": round(regular_price - total_price, 2),
            "items": items,
        }

    def swap_ingredient(self, recipe_id: int, ingredient_id: int, replacement_id: int):
        ingredient = self.recipe_repository.get_ingredient(ingredient_id)
        replacement = self.recipe_repository.get_replacement(replacement_id)
        recipe = self.recipe_repository.get_by_id(recipe_id)

        if ingredient is None or replacement is None or recipe is None:
            raise ValueError("Ingredient, replacement or recipe not found")

        ingredient.name = replacement.name
        ingredient.quantity = replacement.quantity
        ingredient.store = replacement.store
        ingredient.price = replacement.price
        ingredient.note = replacement.note

        self.recipe_repository.db.commit()

        recipe = self.recipe_repository.get_by_id(recipe_id)
        shopping_list = self.build(recipe_id)
        return {"recipe": recipe, "shopping_list": shopping_list}
