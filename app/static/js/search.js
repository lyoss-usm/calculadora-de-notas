document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("course-search-input");
  // We'll use a simple debounce function
  let timeout = null;

  if (!searchInput) return;

  searchInput.addEventListener("input", function (e) {
    clearTimeout(timeout);
    const query = e.target.value.trim();

    timeout = setTimeout(() => {
      if (query.length < 2) {
        // If query is short, maybe show all or nothing?
        // For now, let's just do nothing or clear results if we had a results pane.
        return;
      }
      performSearch(query);
    }, 300);
  });

  async function performSearch(query) {
    try {
      const response = await fetch(
        `/api/search?q=${encodeURIComponent(query)}`
      );
      const results = await response.json();

      // NOTE: How do we display results?
      // The search bar is in the Hero section.
      // Option 1: A dropdown list below the input.
      // Option 2: Filter the main grid if visible.

      // Let's implement a dropdown for now.
      // We need a container for results.

      let resultsContainer = document.getElementById("search-results-dropdown");
      if (!resultsContainer) {
        resultsContainer = document.createElement("div");
        resultsContainer.id = "search-results-dropdown";
        resultsContainer.className = "search-results-dropdown";
        // Append it after the input's parent or inside the hero-search div
        searchInput.parentNode.appendChild(resultsContainer);
      }

      resultsContainer.innerHTML = "";

      if (results.length === 0) {
        const item = document.createElement("div");
        item.className = "search-result-item empty";
        item.textContent = "No se encontraron resultados";
        resultsContainer.appendChild(item);
      } else {
        results.forEach((course) => {
          const item = document.createElement("a");
          item.href = `/curso/${course.code}`;
          item.className = "search-result-item";

          // Simple content
          item.innerHTML = `
                        <div class="result-icon">
                            <!-- We can't easily fetch SVG content here unless inline or img tag -->
                            <!-- Use a generic icon or try to use the icon name if available -->
                            <span>📚</span>
                        </div>
                        <div class="result-info">
                            <div class="result-title">${course.title}</div>
                            <div class="result-code">${course.code}</div>
                        </div>
                    `;
          resultsContainer.appendChild(item);
        });
      }

      resultsContainer.style.display = "block";
    } catch (error) {
      console.error("Search error:", error);
    }
  }

  // Hide dropdown when clicking outside
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".hero-search")) {
      const resultsContainer = document.getElementById(
        "search-results-dropdown"
      );
      if (resultsContainer) {
        resultsContainer.style.display = "none";
      }
    }
  });
});
