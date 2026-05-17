import { useEffect, useState } from "react";
import { api } from "./api";

const screens = {
  home: "home",
  preferences: "preferences",
  recipes: "recipes",
  shopping: "shopping"
};

const defaultPreferences = {
  age: 25,
  weight: 70,
  height: 175,
  goal: "Utrzymać wagę",
  diet_type: "Standardowa",
  allergies: "",
  shopping_mode: "Kilka sklepów"
};

function App() {
  const [activeScreen, setActiveScreen] = useState(screens.home);
  const [dashboard, setDashboard] = useState(null);
  const [recipes, setRecipes] = useState([]);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [preferences, setPreferences] = useState(defaultPreferences);
  const [shoppingList, setShoppingList] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadData() {
    try {
      setIsLoading(true);
      setError("");

      const [dashboardData, preferencesData, recipesData, shoppingListData] =
        await Promise.all([
          api.getDashboard(),
          api.getPreferences(),
          api.getRecipes(),
          api.getShoppingList()
        ]);

      setDashboard(dashboardData);
      setPreferences(preferencesData);
      setRecipes(recipesData);
      const initialRecipeId = recipesData[1]?.id || recipesData[0]?.id;
      if (initialRecipeId) {
        const recipeData = await api.getRecipe(initialRecipeId);
        setSelectedRecipe(recipeData);
      }
      setShoppingList(shoppingListData);
    } catch (loadError) {
      setError("Nie udało się połączyć z backendem. Uruchom API na porcie 8000.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function handleSavePreferences(event) {
    event.preventDefault();
    await api.savePreferences(preferences);
    await loadData();
    setActiveScreen(screens.home);
  }

  async function handleChooseRecipe(recipeId) {
    const recipe = await api.getRecipe(recipeId);
    setSelectedRecipe(recipe);
    setActiveScreen(screens.recipes);
  }

  async function handleSwap(ingredientId, replacementId) {
    if (!selectedRecipe) {
      return;
    }

    const updatedRecipe = await api.swapIngredient(
      selectedRecipe.id,
      ingredientId,
      replacementId
    );

    setSelectedRecipe(updatedRecipe.recipe);
    setShoppingList(updatedRecipe.shopping_list);
  }

  if (isLoading) {
    return <div className="shell loading">Ładowanie aplikacji...</div>;
  }

  return (
    <div className="shell">
      <aside className="sidebar">
        <div>
          <p className="eyebrow">Smart food planner</p>
          <h1>Deal&Meal</h1>
          <p className="muted">
            Prosty prototyp fullstack oparty na ekranach z Figmy.
          </p>
        </div>

        <nav className="nav">
          <button
            className={activeScreen === screens.home ? "active" : ""}
            onClick={() => setActiveScreen(screens.home)}
          >
            Główna
          </button>
          <button
            className={activeScreen === screens.preferences ? "active" : ""}
            onClick={() => setActiveScreen(screens.preferences)}
          >
            Preferencje
          </button>
          <button
            className={activeScreen === screens.recipes ? "active" : ""}
            onClick={() => setActiveScreen(screens.recipes)}
          >
            Przepisy
          </button>
          <button
            className={activeScreen === screens.shopping ? "active" : ""}
            onClick={() => setActiveScreen(screens.shopping)}
          >
            Lista zakupów
          </button>
        </nav>

        <div className="status">
          <span>Backend</span>
          <strong>{error ? "offline" : "online"}</strong>
        </div>
      </aside>

      <main className="phone-frame">
        {error ? <div className="error">{error}</div> : null}
        {activeScreen === screens.home && dashboard ? (
          <HomeScreen dashboard={dashboard} onChooseRecipe={handleChooseRecipe} />
        ) : null}
        {activeScreen === screens.preferences ? (
          <PreferencesScreen
            preferences={preferences}
            setPreferences={setPreferences}
            onSubmit={handleSavePreferences}
          />
        ) : null}
        {activeScreen === screens.recipes && selectedRecipe ? (
          <RecipesScreen recipe={selectedRecipe} onSwap={handleSwap} />
        ) : null}
        {activeScreen === screens.shopping && shoppingList ? (
          <ShoppingScreen shoppingList={shoppingList} />
        ) : null}
      </main>
    </div>
  );
}

function HomeScreen({ dashboard, onChooseRecipe }) {
  return (
    <section className="screen">
      <p className="brand">Deal&Meal</p>
      <h2>Cześć, co dzisiaj zjesz?</h2>

      <div className="hero-card">
        <div>
          <p className="card-label">Posiłek z promocji</p>
          <h3>{dashboard.featured_recipe.name}</h3>
          <p>{dashboard.featured_recipe.description}</p>
        </div>
        <button onClick={() => onChooseRecipe(dashboard.featured_recipe.id)}>
          Zobacz składniki
        </button>
      </div>

      <div className="stats-grid">
        <StatCard label="Kalorie" value={dashboard.stats.calories} />
        <StatCard label="Waga" value={dashboard.stats.weight} />
        <StatCard label="Oszczędności" value={dashboard.stats.savings} />
      </div>

      <div className="section-header">
        <h3>Polecane przepisy</h3>
        <span>~30 min</span>
      </div>

      <div className="recipe-list">
        {dashboard.recommended_recipes.map((recipe) => (
          <button
            key={recipe.id}
            className="recipe-card"
            onClick={() => onChooseRecipe(recipe.id)}
          >
            <div>
              <strong>{recipe.name}</strong>
              <p>{recipe.description}</p>
            </div>
            <div className="price-box">
              <span>{recipe.regular_price} zł</span>
              <strong>{recipe.discounted_price} zł</strong>
            </div>
          </button>
        ))}
      </div>
    </section>
  );
}

function PreferencesScreen({ preferences, setPreferences, onSubmit }) {
  function update(field, value) {
    setPreferences((current) => ({
      ...current,
      [field]: value
    }));
  }

  return (
    <section className="screen">
      <p className="brand">Twoje preferencje</p>
      <h2>Spersonalizuj doświadczenie</h2>

      <form className="form-grid" onSubmit={onSubmit}>
        <label>
          Wiek
          <input
            type="number"
            value={preferences.age}
            onChange={(event) => update("age", Number(event.target.value))}
          />
        </label>
        <label>
          Waga (kg)
          <input
            type="number"
            value={preferences.weight}
            onChange={(event) => update("weight", Number(event.target.value))}
          />
        </label>
        <label>
          Wzrost (cm)
          <input
            type="number"
            value={preferences.height}
            onChange={(event) => update("height", Number(event.target.value))}
          />
        </label>
        <label>
          Cel
          <select
            value={preferences.goal}
            onChange={(event) => update("goal", event.target.value)}
          >
            <option>Schudnąć</option>
            <option>Utrzymać wagę</option>
            <option>Przytyć</option>
          </select>
        </label>
        <label>
          Typ diety
          <select
            value={preferences.diet_type}
            onChange={(event) => update("diet_type", event.target.value)}
          >
            <option>Standardowa</option>
            <option>Wegetariańska</option>
            <option>Wegańska</option>
            <option>Keto</option>
          </select>
        </label>
        <label>
          Tryb zakupów
          <select
            value={preferences.shopping_mode}
            onChange={(event) => update("shopping_mode", event.target.value)}
          >
            <option>Jeden sklep</option>
            <option>Kilka sklepów</option>
          </select>
        </label>
        <label className="full-width">
          Alergie i nietolerancje
          <input
            type="text"
            value={preferences.allergies}
            onChange={(event) => update("allergies", event.target.value)}
            placeholder="np. gluten, laktoza"
          />
        </label>
        <button className="primary" type="submit">
          Zapisz preferencje
        </button>
      </form>
    </section>
  );
}

function RecipesScreen({ recipe, onSwap }) {
  return (
    <section className="screen">
      <p className="brand">Przepis z promocji</p>
      <h2>{recipe.name}</h2>
      <div className="hero-card compact">
        <div>
          <p>{recipe.description}</p>
          <small>
            {recipe.calories} kcal • {recipe.duration_minutes} min • {recipe.portions} porcje
          </small>
        </div>
        <div className="price-stack">
          <strong>{recipe.discounted_price} zł</strong>
          <span>{recipe.regular_price} zł</span>
        </div>
      </div>

      <div className="section-header">
        <h3>Składniki</h3>
        <span>Koszt: {recipe.discounted_price} zł</span>
      </div>

      <div className="ingredient-list">
        {recipe.ingredients.map((ingredient) => (
          <article key={ingredient.id} className="ingredient-card">
            <div>
              <strong>{ingredient.name}</strong>
              <p>
                {ingredient.quantity} • {ingredient.store}
              </p>
            </div>
            <div className="ingredient-actions">
              <span>{ingredient.price} zł</span>
              {ingredient.replacements.length > 0 ? (
                <select
                  defaultValue=""
                  onChange={(event) => {
                    if (event.target.value) {
                      onSwap(ingredient.id, Number(event.target.value));
                    }
                  }}
                >
                  <option value="">Zamień</option>
                  {ingredient.replacements.map((replacement) => (
                    <option key={replacement.id} value={replacement.id}>
                      {replacement.name} - {replacement.price} zł
                    </option>
                  ))}
                </select>
              ) : (
                <small>Najlepsza cena</small>
              )}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function ShoppingScreen({ shoppingList }) {
  return (
    <section className="screen">
      <p className="brand">Twoja lista zakupów</p>
      <h2>{shoppingList.store_name}</h2>

      <div className="hero-card compact">
        <div>
          <p>{shoppingList.address}</p>
          <small>
            {shoppingList.distance} • {shoppingList.walking_time}
          </small>
        </div>
        <div className="price-stack">
          <strong>{shoppingList.total_price} zł</strong>
          <span>{shoppingList.regular_price} zł</span>
        </div>
      </div>

      <div className="section-header">
        <h3>Produkty do kupienia</h3>
        <span>Oszczędzasz {shoppingList.savings} zł</span>
      </div>

      <div className="ingredient-list">
        {shoppingList.items.map((item) => (
          <article key={item.id} className="ingredient-card">
            <div>
              <strong>{item.name}</strong>
              <p>
                {item.quantity} • {item.store}
              </p>
            </div>
            <div className="ingredient-actions">
              <span>{item.price} zł</span>
              <small>{item.note}</small>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function StatCard({ label, value }) {
  return (
    <div className="stat-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

export default App;
