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
        updateContour();
      }
    });
  });

  // Axis Toggle Functionality
  const axisButtons = document.querySelectorAll(".axis-btn");

  axisButtons.forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.preventDefault(); // Prevent accordion expansion if needed
      e.stopPropagation();

      const parent = this.parentElement;
      if (parent.classList.contains("locked")) return;

      // Deactivate siblings
      parent
        .querySelectorAll(".axis-btn")
        .forEach((b) => b.classList.remove("active"));

      // Activate clicked
      this.classList.add("active");

      // Update state
      parent.dataset.state = this.dataset.axis;

      // Trigger contour update
      updateContour();
    });
  });

  function updateToggleVisibility(input) {
    const group = input.closest(".evaluation-input-group");
    const toggle = group.querySelector(".axis-toggle");
    if (!toggle) return;

    if (input.value.trim() !== "") {
      toggle.classList.add("locked");
    } else {
      toggle.classList.remove("locked");
    }
  }

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

    // Get value from input with id "meta-goal-input"
    const goalInput = document.getElementById("meta-goal-input");
    const goalValue = goalInput ? parseFloat(goalInput.value) : 55.0;

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
      body: JSON.stringify({ grades, filled, goal: goalValue }),
    })
      .then((response) => response.json())
      .then((res) => {
        console.log("Calculation results:", res);

        const goalEl = document.querySelector("#goal-grade");
        if (goalEl) {
          goalEl.innerText = goalValue.toString();
        }

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

  const updateContour = debounce(function () {
    if (!courseCode) return;

    // Check if advanced chart is active (optional optimization)
    const chartAdvanced = document.querySelector(".chart-advanced");
    if (chartAdvanced.style.display === "none") return;

    const goalInput = document.getElementById("meta-goal-input");
    const goalValue = goalInput ? parseFloat(goalInput.value) : 55.0;

    const grades = [];
    const x_indices = [];
    const y_indices = [];

    evaluationInputs.forEach((input, index) => {
      const val = input.value.trim();
      const group = input.closest(".evaluation-input-group");
      const toggle = group.querySelector(".axis-toggle");

      if (val === "") {
        grades.push(null);
        if (toggle && !toggle.classList.contains("locked")) {
          const state = toggle.dataset.state; // 'x' or 'y'
          if (state === "x") x_indices.push(index);
          else if (state === "y") y_indices.push(index);
        }
      } else {
        grades.push(parseFloat(val));
      }
    });

    // Extract evaluation names for axis titles
    let xNames = [];
    let yNames = [];

    // We iterate again or store it during the first pass. Since we need names for selected indices:
    // Actually, distinct arrays for names is easier.

    evaluationInputs.forEach((input, index) => {
      const group = input.closest(".evaluation-input-group");
      // The title is in the accordion button, which is up the DOM tree differently
      // structure: .evaluation-group > .evaluation-accordion > .accordion-left > ... .accordion-title
      // But .evaluation-input-group is inside .evaluation-content inside .evaluation-group
      const evaluationGroup = input.closest(".evaluation-group");
      const titleEl = evaluationGroup.querySelector(".accordion-title");
      const title = titleEl ? titleEl.innerText.trim() : `Eval ${index + 1}`;

      if (x_indices.includes(index)) xNames.push(title);
      if (y_indices.includes(index)) yNames.push(title);
    });

    fetch(`/api/grades/${courseCode}/contour`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        grades: grades,
        x_indices: x_indices,
        y_indices: y_indices,
        target_grade: goalValue,
      }),
    })
      .then((r) => r.json())
      .then((data) => {
        console.log("Contour data:", data);
        if (typeof renderAdvancedChart === "function") {
          renderAdvancedChart(data, xNames.join(", "), yNames.join(", "));
        }
      })
      .catch(console.error);
  }, 1000);

  function renderAdvancedChart(data, xTitle, yTitle) {
    const plotDiv = document.getElementById("advanced-chart");
    if (!plotDiv) return;

    // Ensure data.x and data.y are valid arrays
    if (!data.x || !data.y || data.x.length === 0) {
      // Verify if we have no solution or waiting for data
      // Plotly might need an empty trace or clear
      Plotly.purge(plotDiv);
      return;
    }

    const trace = {
      x: data.x,
      y: data.y,
      mode: "lines",
      type: "scatter",
      line: {
        color: "#10b981", // emerald-500
        width: 3,
      },
      name: "Nivel Objetivo",
    };

    const layout = {
      xaxis: {
        title: { text: xTitle, font: { size: 14 } },
        range: [0, 100],
        fixedrange: true, // Prevent zoom/pan per requirements (or at least keeping range [0, 100])
        showgrid: true,
        zeroline: true,
        constrain: "domain",
      },
      yaxis: {
        title: { text: yTitle, font: { size: 14 } },
        range: [0, 100],
        fixedrange: true,
        showgrid: true,
        zeroline: true,
        scaleanchor: "x",
        scaleratio: 1,
        constrain: "domain",
      },
      margin: { t: 40, r: 20, b: 60, l: 60 },
      showlegend: false,
      hovermode: "closest",
    };

    const config = {
      responsive: true,
      displayModeBar: false, // Clean look
    };

    Plotly.newPlot(plotDiv, [trace], layout, config);
  }

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
        } else if (numValue < 0 && value !== "") {
          value = "0";
        }
      }

      this.value = value;
      this.value = value;
      updateToggleVisibility(this);
      saveGrades();
      updateContour();
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
