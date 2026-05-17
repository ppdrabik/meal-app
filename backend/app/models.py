from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    goal = Column(String, nullable=False)
    diet_type = Column(String, nullable=False)
    allergies = Column(String, default="")
    shopping_mode = Column(String, nullable=False)


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    calories = Column(Integer, nullable=False)
    portions = Column(Integer, nullable=False)
    discounted_price = Column(Float, nullable=False)
    regular_price = Column(Float, nullable=False)

    ingredients = relationship("Ingredient", back_populates="recipe")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    store = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    note = Column(String, default="")

    recipe = relationship("Recipe", back_populates="ingredients")
    replacements = relationship("Replacement", back_populates="ingredient")


class Replacement(Base):
    __tablename__ = "replacements"

    id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    store = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    note = Column(String, default="")

    ingredient = relationship("Ingredient", back_populates="replacements")
