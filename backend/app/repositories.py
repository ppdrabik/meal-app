from sqlalchemy.orm import Session, selectinload

from . import models


class PreferenceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_first(self):
        return self.db.query(models.Preference).first()

    def save(self, preference_data: dict):
        preference = self.get_first()
        if preference is None:
            preference = models.Preference(**preference_data)
            self.db.add(preference)
        else:
            for key, value in preference_data.items():
                setattr(preference, key, value)

        self.db.commit()
        self.db.refresh(preference)
        return preference


class RecipeRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self):
        return (
            self.db.query(models.Recipe)
            .options(
                selectinload(models.Recipe.ingredients).selectinload(
                    models.Ingredient.replacements
                )
            )
            .all()
        )

    def get_by_id(self, recipe_id: int):
        return (
            self.db.query(models.Recipe)
            .options(
                selectinload(models.Recipe.ingredients).selectinload(
                    models.Ingredient.replacements
                )
            )
            .filter(models.Recipe.id == recipe_id)
            .first()
        )

    def get_ingredient(self, ingredient_id: int):
        return (
            self.db.query(models.Ingredient)
            .options(selectinload(models.Ingredient.replacements))
            .filter(models.Ingredient.id == ingredient_id)
            .first()
        )

    def get_replacement(self, replacement_id: int):
        return (
            self.db.query(models.Replacement)
            .filter(models.Replacement.id == replacement_id)
            .first()
        )
