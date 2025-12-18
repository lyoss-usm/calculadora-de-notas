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

  evaluationInputs.forEach((input) => {
    input.value = "";
    input.setAttribute("autocomplete", "off");
  });

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
    let filledCount = 0;

    evaluationInputs.forEach((input) => {
      const val = input.value.trim();
      if (val === "") {
        grades.push(0);
        filled.push(false);
      } else {
        grades.push(parseFloat(val));
        filled.push(true);
        filledCount++;
      }
    });

    const totalEvaluations = evaluationInputs.length;
    const progress =
      totalEvaluations > 0
        ? Math.round((filledCount / totalEvaluations) * 100)
        : 0;

    fetch(`/api/grades/${courseCode}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ grades, filled, goal: 55.0 }),
    })
      .then((response) => response.json())
      .then((res) => {
        console.log("Calculation results:", res);

        const currentEl = document.querySelector("#current-grade");
        if (currentEl && res.current_grade !== undefined) {
          currentEl.innerText = res.current_grade;
        }

        const neededEl = document.querySelector("#max-grade");
        if (neededEl) {
          if (res.needed_grade === "--" && res.max_grade >= 55) {
            neededEl.innerText = "Posible";
            neededEl.style.fontSize = "2rem";
          } else if (res.needed_grade === "--") {
            neededEl.innerText = "--";
            neededEl.style.fontSize = "3rem";
          } else {
            neededEl.innerText = res.needed_grade;
            neededEl.style.fontSize = "3rem";
          }
        }

        const progressEl = document.querySelector(".chart-placeholder-label");
        if (progressEl) {
          progressEl.innerText = `Avance: ${progress}%`;
        }
      })
      .catch((error) => {
        console.error("Error saving grades:", error);
      });
  }, 1000);

  evaluationInputs.forEach((input) => {
    input.addEventListener("input", function (e) {
      let value = this.value;

      value = value.replace(/[^0-9]/g, "");

      if (value.length > 3) {
        value = value.slice(0, 3);
      }

      if (value !== "") {
        const numValue = parseInt(value);
        if (numValue > 100) {
          value = "100";
        } else if (numValue < 1 && value !== "") {
          value = "1";
        }
      }

      this.value = value;
      saveGrades();
    });

    input.addEventListener("keypress", function (e) {
      const char = String.fromCharCode(e.which);
      if (!/[0-9]/.test(char) && e.which !== 8) {
        e.preventDefault();
      }
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
