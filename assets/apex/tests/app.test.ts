// @vitest-environment jsdom

import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { mountApex } from "../src/app";

function input(element: HTMLInputElement, value: string): void {
  element.value = value;
  element.dispatchEvent(new Event("input", { bubbles: true }));
}

function change(select: HTMLSelectElement, value: string): void {
  select.value = value;
  select.dispatchEvent(new Event("change", { bubbles: true }));
}

describe("Apex application", () => {
  let root: HTMLElement;
  let unmount: () => void;

  beforeEach(() => {
    document.body.innerHTML = '<main id="apex-app" aria-busy="true"></main>';
    root = document.querySelector<HTMLElement>("#apex-app")!;
    unmount = mountApex(root);
  });

  afterEach(() => unmount());

  it("starts with the length converter and a computed result", () => {
    const left = root.querySelector<HTMLInputElement>("#apex-left-value")!;
    const right = root.querySelector<HTMLInputElement>("#apex-right-value")!;
    const selected = root.querySelector<HTMLButtonElement>('[data-category="length"]')!;

    expect(root.getAttribute("aria-busy")).toBe("false");
    expect(root.querySelector("#apex-category-name")?.textContent).toBe("Length Conversion");
    expect(left.value).toBe("1");
    expect(right.value).toBe("0.1");
    expect(selected.getAttribute("aria-pressed")).toBe("true");
    expect(root.querySelector<HTMLImageElement>(".apex-titlebar__icon")?.src).toContain(
      "/assets/images/apex/app.png",
    );
  });

  it("converts edits in both directions", () => {
    const left = root.querySelector<HTMLInputElement>("#apex-left-value")!;
    const right = root.querySelector<HTMLInputElement>("#apex-right-value")!;

    input(left, "250");
    expect(right.value).toBe("25");

    input(right, "3.5");
    expect(left.value).toBe("35");
  });

  it("recomputes from the most recently edited side when either unit changes", () => {
    const left = root.querySelector<HTMLInputElement>("#apex-left-value")!;
    const right = root.querySelector<HTMLInputElement>("#apex-right-value")!;
    const leftUnit = root.querySelector<HTMLSelectElement>("#apex-left-unit")!;
    const rightUnit = root.querySelector<HTMLSelectElement>("#apex-right-unit")!;

    input(left, "1000");
    change(rightUnit, "meter");
    expect(right.value).toBe("1");

    input(right, "2");
    change(leftUnit, "centimeter");
    expect(right.value).toBe("2");
    expect(left.value).toBe("200");
  });

  it("changes category, resets units, preserves a useful value, focuses, and announces", () => {
    const left = root.querySelector<HTMLInputElement>("#apex-left-value")!;
    input(left, "2");
    root.querySelector<HTMLButtonElement>('[data-category="area"]')!.click();

    expect(root.querySelector("#apex-category-name")?.textContent).toBe("Area Conversion");
    expect(root.querySelector<HTMLSelectElement>("#apex-left-unit")!.value).toBe("square-millimeter");
    expect(root.querySelector<HTMLSelectElement>("#apex-right-unit")!.value).toBe("square-centimeter");
    expect(left.value).toBe("2");
    expect(root.querySelector<HTMLInputElement>("#apex-right-value")!.value).toBe("0.02");
    expect(document.activeElement).toBe(left);
    expect(root.querySelector("#apex-status")?.textContent).toContain("Area:");
  });

  it("activates category buttons from the keyboard", () => {
    const temperature = root.querySelector<HTMLButtonElement>('[data-category="temperature"]')!;
    temperature.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", bubbles: true }));

    expect(root.querySelector("#apex-category-name")?.textContent).toBe("Temperature Conversion");
    expect(temperature.getAttribute("aria-pressed")).toBe("true");
    expect(root.querySelector<HTMLInputElement>("#apex-left-value")).toBe(document.activeElement);

    const power = root.querySelector<HTMLButtonElement>('[data-category="power"]')!;
    power.dispatchEvent(new KeyboardEvent("keydown", { key: " ", bubbles: true }));
    expect(root.querySelector("#apex-category-name")?.textContent).toBe("Power Conversion");
    expect(power.getAttribute("aria-pressed")).toBe("true");
  });

  it("clears the result for empty and invalid input without throwing", () => {
    const left = root.querySelector<HTMLInputElement>("#apex-left-value")!;
    const right = root.querySelector<HTMLInputElement>("#apex-right-value")!;
    const status = root.querySelector<HTMLElement>("#apex-status")!;

    input(left, "");
    expect(right.value).toBe("");
    expect(status.textContent).toBe("Ready");

    input(left, "twelve");
    expect(right.value).toBe("");
    expect(status.textContent).toBe("Invalid number");

    input(left, "1e999");
    expect(right.value).toBe("");
    expect(status.textContent).toBe("Invalid number");

    input(left, "1e308");
    change(root.querySelector<HTMLSelectElement>("#apex-left-unit")!, "kilometer");
    change(root.querySelector<HTMLSelectElement>("#apex-right-unit")!, "millimeter");
    expect(right.value).toBe("");
    expect(status.textContent).toBe("Invalid number");
  });

  it("provides accessible names and a polite status region", () => {
    expect(root.querySelector('nav[aria-label="Conversion categories"]')).not.toBeNull();
    expect(root.querySelector('label[for="apex-left-value"]')?.textContent).toBe("Value");
    expect(root.querySelector('label[for="apex-right-value"]')?.textContent).toBe("Result");
    expect(root.querySelector("#apex-status")?.getAttribute("aria-live")).toBe("polite");
    expect(root.querySelectorAll(".apex-category img[alt='']")).toHaveLength(10);
  });
});
