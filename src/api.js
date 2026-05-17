const API_URL = "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json();
}

export const api = {
  getDashboard() {
    return request("/api/dashboard");
  },
  getPreferences() {
    return request("/api/preferences");
  },
  savePreferences(payload) {
    return request("/api/preferences", {
      method: "PUT",
      body: JSON.stringify(payload)
    });
  },
  getRecipes() {
    return request("/api/recipes");
  },
  getRecipe(id) {
    return request(`/api/recipes/${id}`);
  },
  swapIngredient(recipeId, ingredientId, replacementId) {
    return request(`/api/recipes/${recipeId}/swap`, {
      method: "POST",
      body: JSON.stringify({
        ingredient_id: ingredientId,
        replacement_id: replacementId
      })
    });
  },
  getShoppingList() {
    return request("/api/shopping-list");
  }
};
