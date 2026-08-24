import {
  CONVERSION_CATEGORIES,
  convertValue,
  formatNumber,
  getCategory,
  parseNumericInput,
  type CategoryId,
  type ConversionCategory,
} from "./conversions";

type Side = "left" | "right";

interface AppElements {
  categoryName: HTMLElement;
  leftInput: HTMLInputElement;
  leftUnit: HTMLSelectElement;
  rightInput: HTMLInputElement;
  rightUnit: HTMLSelectElement;
  status: HTMLElement;
}

const ICON_ROOT = "/assets/images/apex";

function categoryButton(category: ConversionCategory, selected: boolean): string {
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

function appMarkup(): string {
  const categories = CONVERSION_CATEGORIES.map((category, index) =>
    categoryButton(category, index === 0),
  ).join("");

  return `
    <section class="apex-window" aria-label="Apex unit converter">
      <header class="apex-titlebar">
        <img class="apex-titlebar__icon" src="${ICON_ROOT}/app.png" width="32" height="32" alt="">
        <h2>Apex</h2>
        <span class="apex-titlebar__controls" aria-hidden="true">
          <span>_</span><span>□</span>
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

function getElements(root: HTMLElement): AppElements {
  const requireElement = <T extends Element>(selector: string): T => {
    const element = root.querySelector<T>(selector);
    if (!element) throw new Error(`Apex is missing required element: ${selector}`);
    return element;
  };

  return {
    categoryName: requireElement("#apex-category-name"),
    leftInput: requireElement("#apex-left-value"),
    leftUnit: requireElement("#apex-left-unit"),
    rightInput: requireElement("#apex-right-value"),
    rightUnit: requireElement("#apex-right-unit"),
    status: requireElement("#apex-status"),
  };
}

function populateSelect(select: HTMLSelectElement, category: ConversionCategory): void {
  select.replaceChildren(
    ...category.units.map((unit) => {
      const option = document.createElement("option");
      option.value = unit.id;
      option.textContent = unit.label;
      return option;
    }),
  );
}

export function mountApex(root: HTMLElement): () => void {
  root.innerHTML = appMarkup();
  root.setAttribute("aria-busy", "false");
  const elements = getElements(root);
  const initialCategory = CONVERSION_CATEGORIES[0];
  if (!initialCategory) throw new Error("Apex needs at least one conversion category");
  let categoryId = initialCategory.id;
  let lastEdited: Side = "left";
  const abortController = new AbortController();
  const eventOptions = { signal: abortController.signal };

  const inputFor = (side: Side) =>
    side === "left" ? elements.leftInput : elements.rightInput;
  const unitFor = (side: Side) =>
    side === "left" ? elements.leftUnit : elements.rightUnit;
  const opposite = (side: Side): Side => (side === "left" ? "right" : "left");

  const recompute = (source: Side, announce = false): void => {
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
      unitFor(target).value,
    );
    if (!Number.isFinite(converted)) {
      inputFor(target).value = "";
      elements.status.textContent = "Invalid number";
      return;
    }

    inputFor(target).value = formatNumber(converted);
    const sourceLabel = unitFor(source).selectedOptions[0]?.textContent ?? "";
    const targetLabel = unitFor(target).selectedOptions[0]?.textContent ?? "";
    elements.status.textContent = announce
      ? `${getCategory(categoryId).label}: ${inputFor(source).value} ${sourceLabel} equals ${inputFor(target).value} ${targetLabel}`
      : "Ready";
  };

  const selectCategory = (nextId: CategoryId, announce: boolean): void => {
    categoryId = nextId;
    const category = getCategory(categoryId);
    elements.categoryName.textContent = `${category.label} Conversion`;
    const headingIcon = root.querySelector<HTMLImageElement>("#apex-category-icon");
    if (headingIcon) headingIcon.src = `${ICON_ROOT}/${category.id}.png`;

    root.querySelectorAll<HTMLButtonElement>(".apex-category").forEach((button) => {
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

  root.querySelectorAll<HTMLButtonElement>(".apex-category").forEach((button) => {
    const activate = (): void => selectCategory(button.dataset.category as CategoryId, true);
    button.addEventListener("click", activate, eventOptions);
    button.addEventListener(
      "keydown",
      (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          activate();
        }
      },
      eventOptions,
    );
  });

  (["left", "right"] as const).forEach((side) => {
    inputFor(side).addEventListener(
      "input",
      () => {
        lastEdited = side;
        recompute(side);
      },
      eventOptions,
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

const defaultRoot = document.querySelector<HTMLElement>("#apex-app");
if (defaultRoot) mountApex(defaultRoot);
