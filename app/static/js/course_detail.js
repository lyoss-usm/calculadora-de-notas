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

    evaluationInputs.forEach((input) => {
      const val = input.value;
      if (val === "") {
        grades.push(null);
      } else {
        grades.push(parseFloat(val));
      }
    });

    fetch(`/api/grades/${courseCode}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ grades }),
    })
      .then((response) => response.json())
      .then((res) => {
        console.log("Calculation results:", res);

        const currentEl = document.querySelector("#current-grade");
        if (currentEl && res.current !== undefined) {
          currentEl.innerText = res.current.toFixed(1);
        }

        const maxEl = document.querySelector("#max-grade");
        if (maxEl && res.max_achievable !== undefined) {
          maxEl.innerText = res.max_achievable.toFixed(1);
        }
      })
      .catch((error) => {
        console.error("Error saving grades:", error);
      });
  }, 1000);

  evaluationInputs.forEach((input) => {
    input.addEventListener("input", function (e) {
      let value = this.value;

      value = value.replace(/[^0-9.]/g, "");

      const parts = value.split(".");
      if (parts.length > 2) {
        value = parts[0] + "." + parts.slice(1).join("");
      }

      if (parts.length === 2) {
        value = parts[0].slice(0, 2) + "." + parts[1].slice(0, 1);
      } else {
        value = value.slice(0, 2);
      }

      if (value !== "" && !value.endsWith(".")) {
        const numValue = parseFloat(value);
        if (numValue > 100) {
          value = "100";
        } else if (numValue < 0) {
          value = "0";
        }
      }

      this.value = value;
      saveGrades();
    });

    input.addEventListener("keypress", function (e) {
      const char = String.fromCharCode(e.which);
      if (!/[0-9.]/.test(char) && e.which !== 8 && e.which !== 46) {
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
