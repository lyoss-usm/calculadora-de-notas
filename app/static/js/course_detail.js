// Course Detail Page - Accordion Functionality

document.addEventListener("DOMContentLoaded", function () {
  // Get all accordion buttons
  const accordionButtons = document.querySelectorAll(".evaluation-accordion");

  accordionButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const evaluationGroup = this.parentElement;
      const isActive = evaluationGroup.classList.contains("active");

      // Close all other accordions
      document.querySelectorAll(".evaluation-group").forEach((group) => {
        group.classList.remove("active");
      });

      // Toggle current accordion
      if (!isActive) {
        evaluationGroup.classList.add("active");
      }
    });
  });

  // Meta toggle buttons (Básico/Avanzado)
  const metaToggles = document.querySelectorAll(".meta-toggle");
  const chartBasic = document.querySelector(".chart-basic");
  const chartAdvanced = document.querySelector(".chart-advanced");

  metaToggles.forEach((toggle) => {
    toggle.addEventListener("click", function () {
      metaToggles.forEach((t) => t.classList.remove("active"));
      this.classList.add("active");

      // Toggle between basic and advanced charts
      if (this.textContent.trim() === "Básico") {
        chartBasic.style.display = "flex";
        chartAdvanced.style.display = "none";
      } else {
        chartBasic.style.display = "none";
        chartAdvanced.style.display = "flex";
      }
    });
  });

  // Auto-update calculations when inputs change
  const evaluationInputs = document.querySelectorAll(".evaluation-input");
  const courseContent = document.querySelector(".course-content");
  const courseCode = courseContent ? courseContent.dataset.courseCode : null;

  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  const saveGrades = debounce(function () {
    if (!courseCode) return;

    const grades = [];
    const filled = [];

    evaluationInputs.forEach((input) => {
      const val = input.value;
      if (val === "") {
        grades.push(null);
        filled.push(false);
      } else {
        grades.push(parseFloat(val));
        filled.push(true);
      }
    });

    fetch(`/api/grades/${courseCode}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ grades, filled }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Grades saved:", data);
      })
      .catch((error) => {
        console.error("Error saving grades:", error);
      });
  }, 1000);

  evaluationInputs.forEach((input) => {
    input.addEventListener("input", function () {
      saveGrades();
    });
  });

  // Goal input change handler
  const goalInput = document.querySelector(".meta-goal-input");

  if (goalInput) {
    goalInput.addEventListener("input", function () {
      // TODO: Recalculate requirements when goal changes
      console.log("Goal changed:", this.value);
    });
  }
});
