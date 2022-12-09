export function enumHasValue<T extends Record<string | number, string | number>>(
	enumType: T,
	value: number | string
): value is T[keyof T] {
	return Object.values(enumType).includes(value);
}
