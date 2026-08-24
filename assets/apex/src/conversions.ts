export type CategoryId =
  | "length"
  | "area"
  | "volume"
  | "mass"
  | "speed"
  | "temperature"
  | "pressure"
  | "time"
  | "energy"
  | "power";

export interface UnitDefinition {
  readonly id: string;
  readonly label: string;
  readonly toBase: (value: number) => number;
  readonly fromBase: (value: number) => number;
}

export interface ConversionCategory {
  readonly id: CategoryId;
  readonly label: string;
  readonly baseUnitId: string;
  readonly units: readonly UnitDefinition[];
}

export type NumericInput =
  | { readonly kind: "empty" }
  | { readonly kind: "invalid" }
  | { readonly kind: "value"; readonly value: number };

interface LinearUnit {
  readonly id: string;
  readonly label: string;
  readonly factor: number;
}

const linearUnit = ({ id, label, factor }: LinearUnit): UnitDefinition => ({
  id,
  label,
  toBase: (value) => value * factor,
  fromBase: (value) => value / factor,
});

const linearCategory = (
  id: CategoryId,
  label: string,
  baseUnitId: string,
  units: readonly LinearUnit[],
): ConversionCategory => ({
  id,
  label,
  baseUnitId,
  units: units.map(linearUnit),
});

export const CONVERSION_CATEGORIES: readonly ConversionCategory[] = [
  linearCategory("length", "Length", "meter", [
    { id: "millimeter", label: "Millimeter", factor: 0.001 },
    { id: "centimeter", label: "Centimeter", factor: 0.01 },
    { id: "meter", label: "Meter", factor: 1 },
    { id: "kilometer", label: "Kilometer", factor: 1000 },
    { id: "inch", label: "Inch", factor: 0.0254 },
    { id: "foot", label: "Foot", factor: 0.3048 },
    { id: "yard", label: "Yard", factor: 0.9144 },
    { id: "mile", label: "Mile", factor: 1609.344 },
    { id: "nautical-mile", label: "Nautical mile", factor: 1852 },
  ]),
  linearCategory("area", "Area", "square-meter", [
    { id: "square-millimeter", label: "Square millimeter", factor: 1e-6 },
    { id: "square-centimeter", label: "Square centimeter", factor: 1e-4 },
    { id: "square-meter", label: "Square meter", factor: 1 },
    { id: "hectare", label: "Hectare", factor: 10000 },
    { id: "square-kilometer", label: "Square kilometer", factor: 1e6 },
    { id: "square-inch", label: "Square inch", factor: 0.00064516 },
    { id: "square-foot", label: "Square foot", factor: 0.09290304 },
    { id: "square-yard", label: "Square yard", factor: 0.83612736 },
    { id: "acre", label: "Acre", factor: 4046.8564224 },
    { id: "square-mile", label: "Square mile", factor: 2589988.110336 },
  ]),
  linearCategory("volume", "Volume", "liter", [
    { id: "milliliter", label: "Milliliter", factor: 0.001 },
    { id: "cubic-centimeter", label: "Cubic centimeter", factor: 0.001 },
    { id: "liter", label: "Liter", factor: 1 },
    { id: "cubic-meter", label: "Cubic meter", factor: 1000 },
    { id: "us-teaspoon", label: "US teaspoon", factor: 0.00492892159375 },
    { id: "us-tablespoon", label: "US tablespoon", factor: 0.01478676478125 },
    { id: "us-fluid-ounce", label: "US fluid ounce", factor: 0.0295735295625 },
    { id: "us-cup", label: "US cup", factor: 0.2365882365 },
    { id: "us-pint", label: "US pint", factor: 0.473176473 },
    { id: "us-quart", label: "US quart", factor: 0.946352946 },
    { id: "us-gallon", label: "US gallon", factor: 3.785411784 },
    { id: "imperial-gallon", label: "Imperial gallon", factor: 4.54609 },
  ]),
  linearCategory("mass", "Mass", "kilogram", [
    { id: "milligram", label: "Milligram", factor: 1e-6 },
    { id: "gram", label: "Gram", factor: 0.001 },
    { id: "kilogram", label: "Kilogram", factor: 1 },
    { id: "metric-tonne", label: "Metric tonne", factor: 1000 },
    { id: "ounce", label: "Ounce", factor: 0.028349523125 },
    { id: "pound", label: "Pound", factor: 0.45359237 },
    { id: "stone", label: "Stone", factor: 6.35029318 },
    { id: "short-ton", label: "Short ton", factor: 907.18474 },
  ]),
  linearCategory("speed", "Speed", "meter-per-second", [
    { id: "meter-per-second", label: "Meter per second", factor: 1 },
    { id: "kilometer-per-hour", label: "Kilometer per hour", factor: 1 / 3.6 },
    { id: "foot-per-second", label: "Foot per second", factor: 0.3048 },
    { id: "mile-per-hour", label: "Mile per hour", factor: 0.44704 },
    { id: "knot", label: "Knot", factor: 1852 / 3600 },
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
        fromBase: (value) => value - 273.15,
      },
      {
        id: "fahrenheit",
        label: "Fahrenheit",
        toBase: (value) => (value + 459.67) * (5 / 9),
        fromBase: (value) => value * (9 / 5) - 459.67,
      },
      { id: "kelvin", label: "Kelvin", toBase: (value) => value, fromBase: (value) => value },
      {
        id: "rankine",
        label: "Rankine",
        toBase: (value) => value * (5 / 9),
        fromBase: (value) => value * (9 / 5),
      },
    ],
  },
  linearCategory("pressure", "Pressure", "pascal", [
    { id: "pascal", label: "Pascal", factor: 1 },
    { id: "kilopascal", label: "Kilopascal", factor: 1000 },
    { id: "megapascal", label: "Megapascal", factor: 1e6 },
    { id: "bar", label: "Bar", factor: 100000 },
    { id: "millibar", label: "Millibar", factor: 100 },
    { id: "atmosphere", label: "Atmosphere", factor: 101325 },
    { id: "torr", label: "Torr", factor: 101325 / 760 },
    { id: "pound-per-square-inch", label: "Pounds per square inch", factor: 6894.757293168361 },
  ]),
  linearCategory("time", "Time", "second", [
    { id: "millisecond", label: "Millisecond", factor: 0.001 },
    { id: "second", label: "Second", factor: 1 },
    { id: "minute", label: "Minute", factor: 60 },
    { id: "hour", label: "Hour", factor: 3600 },
    { id: "day", label: "Day", factor: 86400 },
    { id: "week", label: "Week", factor: 604800 },
    { id: "fortnight", label: "Fortnight", factor: 1209600 },
    { id: "julian-year", label: "Julian year", factor: 31557600 },
  ]),
  linearCategory("energy", "Energy", "joule", [
    { id: "joule", label: "Joule", factor: 1 },
    { id: "kilojoule", label: "Kilojoule", factor: 1000 },
    { id: "calorie", label: "Calorie", factor: 4.184 },
    { id: "kilocalorie", label: "Kilocalorie", factor: 4184 },
    { id: "watt-hour", label: "Watt hour", factor: 3600 },
    { id: "kilowatt-hour", label: "Kilowatt hour", factor: 3.6e6 },
    { id: "foot-pound", label: "Foot-pound", factor: 1.3558179483314004 },
    { id: "british-thermal-unit", label: "British thermal unit", factor: 1055.05585262 },
  ]),
  linearCategory("power", "Power", "watt", [
    { id: "watt", label: "Watt", factor: 1 },
    { id: "kilowatt", label: "Kilowatt", factor: 1000 },
    { id: "megawatt", label: "Megawatt", factor: 1e6 },
    { id: "horsepower-mechanical", label: "Horsepower mechanical", factor: 745.6998715822702 },
    { id: "foot-pound-per-second", label: "Foot-pound per second", factor: 1.3558179483314004 },
    { id: "british-thermal-unit-per-hour", label: "British thermal unit per hour", factor: 1055.05585262 / 3600 },
  ]),
];

const categoriesById = new Map(CONVERSION_CATEGORIES.map((category) => [category.id, category]));

export function getCategory(categoryId: CategoryId): ConversionCategory {
  const category = categoriesById.get(categoryId);
  if (!category) {
    throw new RangeError(`Unknown conversion category: ${categoryId}`);
  }
  return category;
}

export function convertValue(
  categoryId: CategoryId,
  value: number,
  fromUnitId: string,
  toUnitId: string,
): number {
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

const DECIMAL_NUMBER = /^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/;

export function parseNumericInput(input: string): NumericInput {
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

export function formatNumber(value: number): string {
  if (!Number.isFinite(value)) {
    return "";
  }
  if (Object.is(value, -0) || value === 0) {
    return "0";
  }

  const absolute = Math.abs(value);
  if (absolute >= 1e15 || absolute < 1e-9) {
    const [coefficient, exponent] = value.toExponential(14).split("e") as [string, string];
    return `${coefficient.replace(/\.?0+$/, "")}e${Number(exponent)}`;
  }
  return String(Number(value.toPrecision(15)));
}
