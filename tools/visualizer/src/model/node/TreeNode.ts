import { RawNodeDatum } from 'react-d3-tree/lib/types/common';

export type TreeNodeConstructorType = new (
	tokensIds: number[],
	tokens: string[],
	support: number,
	idSet: number[],
	children: TreeNode[]
) => TreeNode;

export abstract class TreeNode implements RawNodeDatum {
	readonly name: '' = '';
	abstract readonly idSetLabel: string;

	constructor(
		public readonly tokensIds: number[],
		public readonly tokens: string[],
		public readonly support: number,
		public readonly idSet: number[],
		public readonly children: TreeNode[]
	) {}

	static fromJson<T extends TreeNodeConstructorType>(json: any, NodeClass: T): TreeNode {
		if (typeof json !== 'object' || json === null || json === undefined) throw new Error('Invalid tree file');

		if (!Array.isArray(json?.tokens_ids))
			throw new Error('Invalid tree file format: tokens_ids is not an array');
		if (json?.tokens_ids.some((id: any) => typeof id !== 'number'))
			throw new Error('Invalid tree file format: tokens_ids contains non-numbers');

		if (!Array.isArray(json?.tokens)) throw new Error('Invalid tree file format: tokens is not an array');
		if (json?.tokens.some((token: any) => typeof token !== 'string'))
			throw new Error('Invalid tree file format: tokens contains non-strings');

		if (typeof json?.support !== 'number')
			throw new Error('Invalid tree file format: support is not a number');

		if (!Array.isArray(json?.id_set)) throw new Error('Invalid tree file format: id_set is not an array');
		if (json?.id_set.some((id: any) => typeof id !== 'number'))
			throw new Error('Invalid tree file format: id_set contains non-numbers');

		if (!Array.isArray(json?.children)) throw new Error('Invalid tree file format: children is not an array');

		return new NodeClass(
			json.tokens_ids,
			json.tokens,
			json.support,
			json.id_set,
			json.children.map((child: any) => TreeNode.fromJson(child, NodeClass))
		);
	}
}
