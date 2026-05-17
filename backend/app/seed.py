from sqlalchemy.orm import Session

from . import models


def seed_database(db: Session):
    if db.query(models.Preference).first():
        return

    preference = models.Preference(
        age=25,
        weight=70,
        height=175,
        goal="Utrzymać wagę",
        diet_type="Standardowa",
        allergies="Bez glutenu",
        shopping_mode="Kilka sklepów",
    )
    db.add(preference)

    carbonara = models.Recipe(
        name="Spaghetti Carbonara",
        description="Klasyczny włoski przepis",
        duration_minutes=25,
        calories=640,
        portions=2,
        discounted_price=28.50,
        regular_price=33.50,
    )
    teriyaki = models.Recipe(
        name="Kurczak Teriyaki",
        description="Z warzywami i ryżem",
        duration_minutes=30,
        calories=580,
        portions=2,
        discounted_price=31.20,
        regular_price=39.00,
    )
    risotto = models.Recipe(
        name="Risotto z warzywami",
        description="Bezglutenowe, fit, idealny obiad",
        duration_minutes=35,
        calories=520,
        portions=2,
        discounted_price=19.60,
        regular_price=28.00,
    )
    db.add_all([carbonara, teriyaki, risotto])
    db.flush()

    ingredients = [
        models.Ingredient(
            recipe_id=risotto.id,
            name="Ryż arborio",
            quantity="300 g",
            store="Marka Premium",
            price=8.50,
            note="-25% promocja",
        ),
        models.Ingredient(
            recipe_id=risotto.id,
            name="Brokuł",
            quantity="200 g",
            store="Biedronka",
            price=4.20,
            note="-30% promocja",
        ),
        models.Ingredient(
            recipe_id=risotto.id,
            name="Parmezan",
            quantity="50 g",
            store="Kaufland",
            price=4.90,
            note="Najlepsza cena",
        ),
        models.Ingredient(
            recipe_id=risotto.id,
            name="Cebula",
            quantity="2 szt.",
            store="Lidl",
            price=2.00,
            note="Regularna cena",
        ),
    ]
    db.add_all(ingredients)
    db.flush()

    replacements = [
        models.Replacement(
            ingredient_id=ingredients[0].id,
            name="Ryż jaśminowy",
            quantity="300 g",
            store="Lidl",
            price=5.99,
            note="-35% promocja",
        ),
        models.Replacement(
            ingredient_id=ingredients[0].id,
            name="Ryż basmati",
            quantity="300 g",
            store="Biedronka",
            price=6.50,
            note="-28% promocja",
        ),
        models.Replacement(
            ingredient_id=ingredients[0].id,
            name="Ryż brązowy",
            quantity="300 g",
            store="Kaufland",
            price=7.20,
            note="-20% promocja",
        ),
    ]
    db.add_all(replacements)
    db.commit()
