export class TokensMapEntry {
	constructor(public readonly id: number, public readonly token: string) {}

	static fromJson(json: any): TokensMapEntry {
		if (typeof json !== 'object' || json === null) throw new Error('Invalid tokens map file');

		const id = parseInt(json?.id);
		if (isNaN(id)) throw new Error('Invalid tokens map file format: id is not a number');
		if (typeof json?.token !== 'string')
			throw new Error('Invalid tokens map file format: token is not a string');

		return new TokensMapEntry(json.id, json.token);
	}
}
