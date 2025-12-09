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

  evaluationInputs.forEach((input) => {
    input.addEventListener("input", function () {
      console.log("Input changed:", this.value);
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
