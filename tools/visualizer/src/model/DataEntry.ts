export class DataEntry {
	constructor(public readonly title: string, public readonly tokens: number[]) {}

	static fromJson(json: any): DataEntry {
		if (typeof json !== 'object' || json === null) throw new Error('Invalid data file');

		if (typeof json?.title !== 'string') throw new Error('Invalid data file format: title is not a string');

		if (!Array.isArray(json?.tokens)) throw new Error('Invalid data file format: tokens is not an array');
		if (json?.tokens.some((token: any) => typeof token !== 'number'))
			throw new Error('Invalid data file format: tokens contains non-numbers');

		return new DataEntry(json.title, json.tokens);
	}
}
