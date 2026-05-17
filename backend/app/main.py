from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .repositories import PreferenceRepository, RecipeRepository
from .schemas import (
    DashboardOut,
    PreferenceIn,
    PreferenceOut,
    RecipeOut,
    RecipeSummaryOut,
    ShoppingListOut,
    SwapRequest,
    SwapResponse,
)
from .seed import seed_database
from .services import DashboardService, PreferenceService, RecipeService, ShoppingListBuilder

app = FastAPI(title="DealMeal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        seed_database(db)
    finally:
        db.close()


@app.get("/api/dashboard", response_model=DashboardOut)
def get_dashboard(db: Session = Depends(get_db)):
    service = DashboardService(RecipeRepository(db))
    return service.get_dashboard()


@app.get("/api/preferences", response_model=PreferenceOut)
def get_preferences(db: Session = Depends(get_db)):
    service = PreferenceService(PreferenceRepository(db))
    preference = service.get_preferences()
    if preference is None:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return preference


@app.put("/api/preferences", response_model=PreferenceOut)
def save_preferences(payload: PreferenceIn, db: Session = Depends(get_db)):
    service = PreferenceService(PreferenceRepository(db))
    return service.save_preferences(payload.model_dump())


@app.get("/api/recipes", response_model=list[RecipeSummaryOut])
def list_recipes(db: Session = Depends(get_db)):
    service = RecipeService(RecipeRepository(db))
    return service.list_recipes()


@app.get("/api/recipes/{recipe_id}", response_model=RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    service = RecipeService(RecipeRepository(db))
    recipe = service.get_recipe(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.get("/api/shopping-list", response_model=ShoppingListOut)
def get_shopping_list(db: Session = Depends(get_db)):
    builder = ShoppingListBuilder(RecipeRepository(db))
    return builder.build(recipe_id=3)


@app.post("/api/recipes/{recipe_id}/swap", response_model=SwapResponse)
def swap_ingredient(recipe_id: int, payload: SwapRequest, db: Session = Depends(get_db)):
    builder = ShoppingListBuilder(RecipeRepository(db))
    try:
        return builder.swap_ingredient(recipe_id, payload.ingredient_id, payload.replacement_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
