from pydantic import BaseModel


class ReplacementOut(BaseModel):
    id: int
    name: str
    quantity: str
    store: str
    price: float
    note: str

    class Config:
        from_attributes = True


class IngredientOut(BaseModel):
    id: int
    name: str
    quantity: str
    store: str
    price: float
    note: str
    replacements: list[ReplacementOut]

    class Config:
        from_attributes = True


class RecipeSummaryOut(BaseModel):
    id: int
    name: str
    description: str
    duration_minutes: int
    discounted_price: float
    regular_price: float


class RecipeOut(RecipeSummaryOut):
    calories: int
    portions: int
    ingredients: list[IngredientOut]

    class Config:
        from_attributes = True


class PreferenceIn(BaseModel):
    age: int
    weight: int
    height: int
    goal: str
    diet_type: str
    allergies: str
    shopping_mode: str


class PreferenceOut(PreferenceIn):
    id: int

    class Config:
        from_attributes = True


class ShoppingItemOut(BaseModel):
    id: int
    name: str
    quantity: str
    store: str
    price: float
    note: str


class ShoppingListOut(BaseModel):
    store_name: str
    address: str
    distance: str
    walking_time: str
    total_price: float
    regular_price: float
    savings: float
    items: list[ShoppingItemOut]


class DashboardOut(BaseModel):
    featured_recipe: RecipeSummaryOut
    recommended_recipes: list[RecipeSummaryOut]
    stats: dict[str, str]


class SwapRequest(BaseModel):
    ingredient_id: int
    replacement_id: int


class SwapResponse(BaseModel):
    recipe: RecipeOut
    shopping_list: ShoppingListOut
