"use strict";
(() => {
  // assets/apex/src/conversions.ts
  var linearUnit = ({ id, label, factor }) => ({
    id,
    label,
    toBase: (value) => value * factor,
    fromBase: (value) => value / factor
  });
  var linearCategory = (id, label, baseUnitId, units) => ({
    id,
    label,
    baseUnitId,
    units: units.map(linearUnit)
  });
  var CONVERSION_CATEGORIES = [
    linearCategory("length", "Length", "meter", [
      { id: "millimeter", label: "Millimeter", factor: 1e-3 },
      { id: "centimeter", label: "Centimeter", factor: 0.01 },
      { id: "meter", label: "Meter", factor: 1 },
      { id: "kilometer", label: "Kilometer", factor: 1e3 },
      { id: "inch", label: "Inch", factor: 0.0254 },
      { id: "foot", label: "Foot", factor: 0.3048 },
      { id: "yard", label: "Yard", factor: 0.9144 },
      { id: "mile", label: "Mile", factor: 1609.344 },
      { id: "nautical-mile", label: "Nautical mile", factor: 1852 }
    ]),
    linearCategory("area", "Area", "square-meter", [
      { id: "square-millimeter", label: "Square millimeter", factor: 1e-6 },
      { id: "square-centimeter", label: "Square centimeter", factor: 1e-4 },
      { id: "square-meter", label: "Square meter", factor: 1 },
      { id: "hectare", label: "Hectare", factor: 1e4 },
      { id: "square-kilometer", label: "Square kilometer", factor: 1e6 },
      { id: "square-inch", label: "Square inch", factor: 64516e-8 },
      { id: "square-foot", label: "Square foot", factor: 0.09290304 },
      { id: "square-yard", label: "Square yard", factor: 0.83612736 },
      { id: "acre", label: "Acre", factor: 4046.8564224 },
      { id: "square-mile", label: "Square mile", factor: 2589988110336e-6 }
    ]),
    linearCategory("volume", "Volume", "liter", [
      { id: "milliliter", label: "Milliliter", factor: 1e-3 },
      { id: "cubic-centimeter", label: "Cubic centimeter", factor: 1e-3 },
      { id: "liter", label: "Liter", factor: 1 },
      { id: "cubic-meter", label: "Cubic meter", factor: 1e3 },
      { id: "us-teaspoon", label: "US teaspoon", factor: 0.00492892159375 },
      { id: "us-tablespoon", label: "US tablespoon", factor: 0.01478676478125 },
      { id: "us-fluid-ounce", label: "US fluid ounce", factor: 0.0295735295625 },
      { id: "us-cup", label: "US cup", factor: 0.2365882365 },
      { id: "us-pint", label: "US pint", factor: 0.473176473 },
      { id: "us-quart", label: "US quart", factor: 0.946352946 },
      { id: "us-gallon", label: "US gallon", factor: 3.785411784 },
      { id: "imperial-gallon", label: "Imperial gallon", factor: 4.54609 }
    ]),
    linearCategory("mass", "Mass", "kilogram", [
      { id: "milligram", label: "Milligram", factor: 1e-6 },
      { id: "gram", label: "Gram", factor: 1e-3 },
      { id: "kilogram", label: "Kilogram", factor: 1 },
      { id: "metric-tonne", label: "Metric tonne", factor: 1e3 },
      { id: "ounce", label: "Ounce", factor: 0.028349523125 },
      { id: "pound", label: "Pound", factor: 0.45359237 },
      { id: "stone", label: "Stone", factor: 6.35029318 },
      { id: "short-ton", label: "Short ton", factor: 907.18474 }
    ]),
    linearCategory("speed", "Speed", "meter-per-second", [
      { id: "meter-per-second", label: "Meter per second", factor: 1 },
      { id: "kilometer-per-hour", label: "Kilometer per hour", factor: 1 / 3.6 },
      { id: "foot-per-second", label: "Foot per second", factor: 0.3048 },
      { id: "mile-per-hour", label: "Mile per hour", factor: 0.44704 },
      { id: "knot", label: "Knot", factor: 1852 / 3600 }
    ]),
    {
      id: "temperature",
      label: "Temperature",
      baseUnitId: "kelvin",
      units: [
        {
          id: "celsius",
          label: "Celsius",
          toBase: (value) => value + 273.15,
          fromBase: (value) => value - 273.15
        },
        {
          id: "fahrenheit",
          label: "Fahrenheit",
          toBase: (value) => (value + 459.67) * (5 / 9),
          fromBase: (value) => value * (9 / 5) - 459.67
        },
        { id: "kelvin", label: "Kelvin", toBase: (value) => value, fromBase: (value) => value },
        {
          id: "rankine",
          label: "Rankine",
          toBase: (value) => value * (5 / 9),
          fromBase: (value) => value * (9 / 5)
        }
      ]
    },
    linearCategory("pressure", "Pressure", "pascal", [
      { id: "pascal", label: "Pascal", factor: 1 },
      { id: "kilopascal", label: "Kilopascal", factor: 1e3 },
      { id: "megapascal", label: "Megapascal", factor: 1e6 },
      { id: "bar", label: "Bar", factor: 1e5 },
      { id: "millibar", label: "Millibar", factor: 100 },
      { id: "atmosphere", label: "Atmosphere", factor: 101325 },
      { id: "torr", label: "Torr", factor: 101325 / 760 },
      { id: "pound-per-square-inch", label: "Pounds per square inch", factor: 6894.757293168361 }
    ]),
    linearCategory("time", "Time", "second", [
      { id: "millisecond", label: "Millisecond", factor: 1e-3 },
      { id: "second", label: "Second", factor: 1 },
      { id: "minute", label: "Minute", factor: 60 },
      { id: "hour", label: "Hour", factor: 3600 },
      { id: "day", label: "Day", factor: 86400 },
      { id: "week", label: "Week", factor: 604800 },
      { id: "fortnight", label: "Fortnight", factor: 1209600 },
      { id: "julian-year", label: "Julian year", factor: 31557600 }
    ]),
    linearCategory("energy", "Energy", "joule", [
      { id: "joule", label: "Joule", factor: 1 },
      { id: "kilojoule", label: "Kilojoule", factor: 1e3 },
      { id: "calorie", label: "Calorie", factor: 4.184 },
      { id: "kilocalorie", label: "Kilocalorie", factor: 4184 },
      { id: "watt-hour", label: "Watt hour", factor: 3600 },
      { id: "kilowatt-hour", label: "Kilowatt hour", factor: 36e5 },
      { id: "foot-pound", label: "Foot-pound", factor: 1.3558179483314003 },
      { id: "british-thermal-unit", label: "British thermal unit", factor: 1055.05585262 }
    ]),
    linearCategory("power", "Power", "watt", [
      { id: "watt", label: "Watt", factor: 1 },
      { id: "kilowatt", label: "Kilowatt", factor: 1e3 },
      { id: "megawatt", label: "Megawatt", factor: 1e6 },
      { id: "horsepower-mechanical", label: "Horsepower mechanical", factor: 745.6998715822702 },
      { id: "foot-pound-per-second", label: "Foot-pound per second", factor: 1.3558179483314003 },
      { id: "british-thermal-unit-per-hour", label: "British thermal unit per hour", factor: 1055.05585262 / 3600 }
    ])
  ];
  var categoriesById = new Map(CONVERSION_CATEGORIES.map((category) => [category.id, category]));
  function getCategory(categoryId) {
    const category = categoriesById.get(categoryId);
    if (!category) {
      throw new RangeError(`Unknown conversion category: ${categoryId}`);
    }
    return category;
  }
  function convertValue(categoryId, value, fromUnitId, toUnitId) {
    if (!Number.isFinite(value)) {
      throw new RangeError("Conversion value must be finite");
    }
    const category = getCategory(categoryId);
    const fromUnit = category.units.find((unit) => unit.id === fromUnitId);
    const toUnit = category.units.find((unit) => unit.id === toUnitId);
    if (!fromUnit) {
      throw new RangeError(`Unknown ${categoryId} unit: ${fromUnitId}`);
    }
    if (!toUnit) {
      throw new RangeError(`Unknown ${categoryId} unit: ${toUnitId}`);
    }
    return toUnit.fromBase(fromUnit.toBase(value));
  }
  var DECIMAL_NUMBER = /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/;
  function parseNumericInput(input) {
    const trimmed = input.trim();
    if (trimmed === "") {
      return { kind: "empty" };
    }
    if (!DECIMAL_NUMBER.test(trimmed)) {
      return { kind: "invalid" };
    }
    const value = Number(trimmed);
    return Number.isFinite(value) ? { kind: "value", value } : { kind: "invalid" };
  }
  function formatNumber(value) {
    if (!Number.isFinite(value)) {
      return "";
    }
    if (Object.is(value, -0) || value === 0) {
      return "0";
    }
    const absolute = Math.abs(value);
    if (absolute >= 1e15 || absolute < 1e-9) {
      const [coefficient, exponent] = value.toExponential(14).split("e");
      return `${coefficient.replace(/\.?0+$/, "")}e${Number(exponent)}`;
    }
    return String(Number(value.toPrecision(15)));
  }

  // assets/apex/src/app.ts
  var ICON_ROOT = "/assets/images/apex";
  function categoryButton(category, selected) {
    return `
    <button
      class="apex-category${selected ? " is-selected" : ""}"
      type="button"
      data-category="${category.id}"
      aria-pressed="${selected}"
    >
      <img src="${ICON_ROOT}/${category.id}.png" width="32" height="32" alt="" aria-hidden="true">
      <span>${category.label}</span>
    </button>`;
  }
  function appMarkup() {
    const categories = CONVERSION_CATEGORIES.map(
      (category, index) => categoryButton(category, index === 0)
    ).join("");
    return `
    <section class="apex-window" aria-label="Apex unit converter">
      <header class="apex-titlebar">
        <img class="apex-titlebar__icon" src="${ICON_ROOT}/app.png" width="32" height="32" alt="">
        <h2>Apex</h2>
        <span class="apex-titlebar__controls" aria-hidden="true">
          <span>_</span><span>\u25A1</span>
        </span>
      </header>
      <div class="apex-menubar" aria-label="Application menu">
        <span><u>F</u>ile</span><span><u>H</u>elp</span>
      </div>
      <div class="apex-workspace">
        <nav class="apex-categories" aria-label="Conversion categories">
          ${categories}
        </nav>
        <section class="apex-converter" aria-labelledby="apex-category-name">
          <div class="apex-converter__heading">
            <img id="apex-category-icon" width="32" height="32" alt="" aria-hidden="true">
            <h3 id="apex-category-name"></h3>
          </div>
          <div class="apex-inset apex-fields">
            <div class="apex-field-row">
              <label for="apex-left-value">Value</label>
              <input id="apex-left-value" type="text" inputmode="decimal" autocomplete="off" spellcheck="false">
              <label class="apex-sr-only" for="apex-left-unit">First unit</label>
              <select id="apex-left-unit"></select>
            </div>
            <div class="apex-equals" aria-hidden="true">=</div>
            <div class="apex-field-row">
              <label for="apex-right-value">Result</label>
              <input id="apex-right-value" type="text" inputmode="decimal" autocomplete="off" spellcheck="false">
              <label class="apex-sr-only" for="apex-right-unit">Second unit</label>
              <select id="apex-right-unit"></select>
            </div>
          </div>
        </section>
      </div>
      <footer class="apex-statusbar">
        <span id="apex-status" role="status" aria-live="polite" aria-atomic="true">Ready</span>
        <span aria-hidden="true">NUM</span>
      </footer>
    </section>`;
  }
  function getElements(root) {
    const requireElement = (selector) => {
      const element = root.querySelector(selector);
      if (!element) throw new Error(`Apex is missing required element: ${selector}`);
      return element;
    };
    return {
      categoryName: requireElement("#apex-category-name"),
      leftInput: requireElement("#apex-left-value"),
      leftUnit: requireElement("#apex-left-unit"),
      rightInput: requireElement("#apex-right-value"),
      rightUnit: requireElement("#apex-right-unit"),
      status: requireElement("#apex-status")
    };
  }
  function populateSelect(select, category) {
    select.replaceChildren(
      ...category.units.map((unit) => {
        const option = document.createElement("option");
        option.value = unit.id;
        option.textContent = unit.label;
        return option;
      })
    );
  }
  function mountApex(root) {
    root.innerHTML = appMarkup();
    root.setAttribute("aria-busy", "false");
    const elements = getElements(root);
    const initialCategory = CONVERSION_CATEGORIES[0];
    if (!initialCategory) throw new Error("Apex needs at least one conversion category");
    let categoryId = initialCategory.id;
    let lastEdited = "left";
    const abortController = new AbortController();
    const eventOptions = { signal: abortController.signal };
    const inputFor = (side) => side === "left" ? elements.leftInput : elements.rightInput;
    const unitFor = (side) => side === "left" ? elements.leftUnit : elements.rightUnit;
    const opposite = (side) => side === "left" ? "right" : "left";
    const recompute = (source, announce = false) => {
      const target = opposite(source);
      const parsed = parseNumericInput(inputFor(source).value);
      if (parsed.kind === "empty") {
        inputFor(target).value = "";
        elements.status.textContent = "Ready";
        return;
      }
      if (parsed.kind === "invalid") {
        inputFor(target).value = "";
        elements.status.textContent = "Invalid number";
        return;
      }
      const converted = convertValue(
        categoryId,
        parsed.value,
        unitFor(source).value,
        unitFor(target).value
      );
      if (!Number.isFinite(converted)) {
        inputFor(target).value = "";
        elements.status.textContent = "Invalid number";
        return;
      }
      inputFor(target).value = formatNumber(converted);
      const sourceLabel = unitFor(source).selectedOptions[0]?.textContent ?? "";
      const targetLabel = unitFor(target).selectedOptions[0]?.textContent ?? "";
      elements.status.textContent = announce ? `${getCategory(categoryId).label}: ${inputFor(source).value} ${sourceLabel} equals ${inputFor(target).value} ${targetLabel}` : "Ready";
    };
    const selectCategory = (nextId, announce) => {
      categoryId = nextId;
      const category = getCategory(categoryId);
      elements.categoryName.textContent = `${category.label} Conversion`;
      const headingIcon = root.querySelector("#apex-category-icon");
      if (headingIcon) headingIcon.src = `${ICON_ROOT}/${category.id}.png`;
      root.querySelectorAll(".apex-category").forEach((button) => {
        const selected = button.dataset.category === category.id;
        button.classList.toggle("is-selected", selected);
        button.setAttribute("aria-pressed", String(selected));
      });
      populateSelect(elements.leftUnit, category);
      populateSelect(elements.rightUnit, category);
      const firstUnit = category.units[0];
      if (!firstUnit) throw new Error(`${category.label} needs at least one unit`);
      elements.leftUnit.value = firstUnit.id;
      elements.rightUnit.value = category.units[1]?.id ?? firstUnit.id;
      lastEdited = "left";
      recompute("left", announce);
      if (announce) elements.leftInput.focus();
    };
    root.querySelectorAll(".apex-category").forEach((button) => {
      const activate = () => selectCategory(button.dataset.category, true);
      button.addEventListener("click", activate, eventOptions);
      button.addEventListener(
        "keydown",
        (event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            activate();
          }
        },
        eventOptions
      );
    });
    ["left", "right"].forEach((side) => {
      inputFor(side).addEventListener(
        "input",
        () => {
          lastEdited = side;
          recompute(side);
        },
        eventOptions
      );
      unitFor(side).addEventListener("change", () => recompute(lastEdited, true), eventOptions);
    });
    elements.leftInput.value = "1";
    selectCategory(categoryId, false);
    return () => {
      abortController.abort();
      root.replaceChildren();
      root.setAttribute("aria-busy", "false");
    };
  }
  var defaultRoot = document.querySelector("#apex-app");
  if (defaultRoot) mountApex(defaultRoot);
})();
