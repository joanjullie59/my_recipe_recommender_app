
async function loadHistory() {
  const historyDiv = document.getElementById('searchHistory');
  if (!historyDiv) return;

  historyDiv.innerHTML = 'Loading search history...';

  try {
    const response = await fetch('/search-history', { credentials: 'include' });
    if (!response.ok) {
      throw new Error(`Status ${response.status}`);
    }
    const data = await response.json();

    if (data.history && data.history.length > 0) {
      historyDiv.innerHTML = data.history.map(item =>
        `<div class="history-item">${item}</div>`).join('');
    } else {
      historyDiv.innerHTML = '<p>No search history found.</p>';
    }
  } catch (error) {
    historyDiv.innerHTML = `<p class="error">Failed to load history: ${error.message}</p>`;
  }
}

function setupEventListeners() {
  const getRecipesBtn = document.getElementById('getRecipesBtn');
  if (!getRecipesBtn) {
    console.error('Button with id "getRecipesBtn" not found in DOM');
    return;
  }

  getRecipesBtn.addEventListener('click', async (event) => {
    event.preventDefault();

    const ingredients = document.getElementById('ingredientsInput').value.trim();
    const diet = document.getElementById('dietSelect').value;
    const cuisine = document.getElementById('cuisineSelect').value;

    if (!ingredients) {
      alert('Please enter some ingredients!');
      return;
    }

    const regexIngredients = /^[a-zA-Z ,]+$/;
    if (!regexIngredients.test(ingredients)) {
      alert('Ingredients should contain only letters, commas, and spaces.');
      return;
    }

    const allowedDiets = ['', 'vegetarian', 'vegan', 'gluten-free'];
    if (!allowedDiets.includes(diet)) {
      alert('Invalid dietary preference selected.');
      return;
    }

    const allowedCuisines = ['', 'Italian', 'Mexican', 'Indian', 'Kenyan'];
    if (!allowedCuisines.includes(cuisine)) {
      alert('Invalid cuisine preference selected.');
      return;
    }

    const recipesDiv = document.getElementById('recipes');
    recipesDiv.innerHTML = `<div class="spinner" title="Loading..."></div><span> Generating recipes from OpenAI...</span>`;

    try {
      const response = await fetch('/recipes', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ ingredients, diet, cuisine }),
        credentials: 'include' // keep cookies/session
      });

      if (!response.ok) {
        const contentType = response.headers.get('content-type') || '';
        let errorMsg = response.statusText;
        if (contentType.includes('application/json')) {
          const data = await response.json();
          errorMsg = data.error || JSON.stringify(data);
        } else {
          errorMsg = await response.text();
        }
        throw new Error(`Error ${response.status}: ${errorMsg}`);
      }

      const data = await response.json();

      if (data.recipes && data.recipes.length > 0) {
        // Display AI-generated recipes (expected from OpenAI backend)
        recipesDiv.innerHTML = data.recipes.map(recipe =>
          `<div class="recipe-card">
             <h3>${recipe.name || 'Recipe'}</h3>
             <p>${recipe.description || ''}</p>
             <strong>Ingredients:</strong>
             <ul>${(recipe.ingredients || []).map(i => `<li>${i}</li>`).join('')}</ul>
             <strong>Instructions:</strong>
             <ol>${(recipe.instructions || []).map(step => `<li>${step}</li>`).join('')}</ol>
           </div>`
        ).join('');
      } else {
        recipesDiv.innerHTML = '<p>No recipes found from AI.</p>';
      }

    } catch (error) {
      recipesDiv.innerHTML = `<p class="error">An error occurred: ${error.message}</p>`;
    }
  });

  window.onload = loadHistory;
}

if (document.readyState !== 'loading') {
  setupEventListeners();
} else if (document.addEventListener) {
  document.addEventListener('DOMContentLoaded', setupEventListeners);
} else {
  document.attachEvent('onreadystatechange', function () {
    if (document.readyState === 'complete') setupEventListeners();
  });
}

