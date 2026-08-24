import { describe, expect, it } from "vitest";

import {
  CONVERSION_CATEGORIES,
  convertValue,
  formatNumber,
  getCategory,
  parseNumericInput,
  type CategoryId,
} from "../src/conversions";

const BASE_VALUES: Record<CategoryId, Record<string, number>> = {
  length: {
    millimeter: 0.001,
    centimeter: 0.01,
    meter: 1,
    kilometer: 1000,
    inch: 0.0254,
    foot: 0.3048,
    yard: 0.9144,
    mile: 1609.344,
    "nautical-mile": 1852,
  },
  area: {
    "square-millimeter": 1e-6,
    "square-centimeter": 1e-4,
    "square-meter": 1,
    hectare: 10000,
    "square-kilometer": 1e6,
    "square-inch": 0.00064516,
    "square-foot": 0.09290304,
    "square-yard": 0.83612736,
    acre: 4046.8564224,
    "square-mile": 2589988.110336,
  },
  volume: {
    milliliter: 0.001,
    "cubic-centimeter": 0.001,
    liter: 1,
    "cubic-meter": 1000,
    "us-teaspoon": 0.00492892159375,
    "us-tablespoon": 0.01478676478125,
    "us-fluid-ounce": 0.0295735295625,
    "us-cup": 0.2365882365,
    "us-pint": 0.473176473,
    "us-quart": 0.946352946,
    "us-gallon": 3.785411784,
    "imperial-gallon": 4.54609,
  },
  mass: {
    milligram: 1e-6,
    gram: 0.001,
    kilogram: 1,
    "metric-tonne": 1000,
    ounce: 0.028349523125,
    pound: 0.45359237,
    stone: 6.35029318,
    "short-ton": 907.18474,
  },
  speed: {
    "meter-per-second": 1,
    "kilometer-per-hour": 1 / 3.6,
    "foot-per-second": 0.3048,
    "mile-per-hour": 0.44704,
    knot: 1852 / 3600,
  },
  temperature: {
    celsius: 274.15,
    fahrenheit: 255.92777777777778,
    kelvin: 1,
    rankine: 5 / 9,
  },
  pressure: {
    pascal: 1,
    kilopascal: 1000,
    megapascal: 1e6,
    bar: 100000,
    millibar: 100,
    atmosphere: 101325,
    torr: 101325 / 760,
    "pound-per-square-inch": 6894.757293168361,
  },
  time: {
    millisecond: 0.001,
    second: 1,
    minute: 60,
    hour: 3600,
    day: 86400,
    week: 604800,
    fortnight: 1209600,
    "julian-year": 31557600,
  },
  energy: {
    joule: 1,
    kilojoule: 1000,
    calorie: 4.184,
    kilocalorie: 4184,
    "watt-hour": 3600,
    "kilowatt-hour": 3.6e6,
    "foot-pound": 1.3558179483314004,
    "british-thermal-unit": 1055.05585262,
  },
  power: {
    watt: 1,
    kilowatt: 1000,
    megawatt: 1e6,
    "horsepower-mechanical": 745.6998715822702,
    "foot-pound-per-second": 1.3558179483314004,
    "british-thermal-unit-per-hour": 1055.05585262 / 3600,
  },
};

const closeTo = (actual: number, expected: number): void => {
  const tolerance = Math.max(1e-12, Math.abs(expected) * 1e-12);
  expect(Math.abs(actual - expected)).toBeLessThanOrEqual(tolerance);
};

describe("conversion catalog", () => {
  it("contains all ten categories in the specified order", () => {
    expect(CONVERSION_CATEGORIES.map(({ id }) => id)).toEqual([
      "length",
      "area",
      "volume",
      "mass",
      "speed",
      "temperature",
      "pressure",
      "time",
      "energy",
      "power",
    ]);
  });

  it.each(CONVERSION_CATEGORIES)("converts every $label unit to and from its base", (category) => {
    const expectedUnits = BASE_VALUES[category.id];
    expect(category.units.map(({ id }) => id)).toEqual(Object.keys(expectedUnits));

    for (const unit of category.units) {
      const expectedBase = expectedUnits[unit.id];
      expect(expectedBase).toBeDefined();
      closeTo(convertValue(category.id, 1, unit.id, category.baseUnitId), expectedBase!);
      closeTo(convertValue(category.id, expectedBase!, category.baseUnitId, unit.id), 1);
    }
  });

  it.each(CONVERSION_CATEGORIES)("round-trips every $label unit pair", (category) => {
    for (const from of category.units) {
      for (const to of category.units) {
        for (const original of [-123.456789, 0, 0.0000314159, 987654.321]) {
          const converted = convertValue(category.id, original, from.id, to.id);
          const roundTrip = convertValue(category.id, converted, to.id, from.id);
          closeTo(roundTrip, original);
        }
      }
    }
  });
});

describe("conversion landmarks", () => {
  it.each([
    ["length", 1, "mile", "kilometer", 1.609344],
    ["area", 1, "acre", "square-meter", 4046.8564224],
    ["volume", 1, "us-gallon", "liter", 3.785411784],
    ["mass", 1, "pound", "kilogram", 0.45359237],
    ["speed", 60, "mile-per-hour", "meter-per-second", 26.8224],
    ["temperature", 32, "fahrenheit", "celsius", 0],
    ["pressure", 1, "atmosphere", "pascal", 101325],
    ["time", 1, "day", "second", 86400],
    ["power", 1, "horsepower-mechanical", "watt", 745.6998715822702],
  ] as const)("converts %s landmark", (category, value, from, to, expected) => {
    closeTo(convertValue(category, value, from, to), expected);
  });

  it("converts one kilowatt hour to 3.6 megajoules", () => {
    closeTo(convertValue("energy", 1, "kilowatt-hour", "joule") / 1e6, 3.6);
  });

  it("handles affine temperature landmarks", () => {
    closeTo(convertValue("temperature", 0, "celsius", "kelvin"), 273.15);
    closeTo(convertValue("temperature", 491.67, "rankine", "fahrenheit"), 32);
  });
});

describe("numeric input parsing", () => {
  it.each(["", "  ", "\t\n"])("treats %j as empty", (input) => {
    expect(parseNumericInput(input)).toEqual({ kind: "empty" });
  });

  it.each([
    ["-42", -42],
    ["+.5", 0.5],
    ["12.", 12],
    ["  -1.25e+3  ", -1250],
    ["6.022E-23", 6.022e-23],
  ])("parses %s as a finite decimal", (input, expected) => {
    expect(parseNumericInput(input)).toEqual({ kind: "value", value: expected });
  });

  it.each(["NaN", "Infinity", "1e309", "0x10", "1,000", "1 2", ".", "+", "1e", "--1"])(
    "rejects %s",
    (input) => {
      expect(parseNumericInput(input)).toEqual({ kind: "invalid" });
    },
  );
});

describe("result formatting", () => {
  it.each([
    [0, "0"],
    [-0, "0"],
    [1 / 3, "0.333333333333333"],
    [0.1 + 0.2, "0.3"],
    [-12.5, "-12.5"],
    [1.2345678901234567, "1.23456789012346"],
    [1e-10, "1e-10"],
    [1.2e15, "1.2e15"],
  ])("formats %s without floating-point noise", (input, expected) => {
    expect(formatNumber(input)).toBe(expected);
  });

  it.each([Number.NaN, Number.POSITIVE_INFINITY, Number.NEGATIVE_INFINITY])(
    "formats non-finite %s as empty",
    (input) => expect(formatNumber(input)).toBe(""),
  );
});

describe("API validation", () => {
  it("rejects non-finite conversion values", () => {
    expect(() => convertValue("length", Number.POSITIVE_INFINITY, "meter", "foot")).toThrow(RangeError);
  });

  it("rejects unknown units", () => {
    expect(() => convertValue("length", 1, "parsec", "meter")).toThrow("Unknown length unit: parsec");
    expect(() => convertValue("length", 1, "meter", "parsec")).toThrow("Unknown length unit: parsec");
  });

  it("looks up categories", () => {
    expect(getCategory("mass").baseUnitId).toBe("kilogram");
  });
});
