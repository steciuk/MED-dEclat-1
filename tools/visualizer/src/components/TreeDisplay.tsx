import React, { useEffect, useState } from 'react';
import Tree from 'react-d3-tree';
import { CustomNodeElementProps } from 'react-d3-tree/lib/types/common';

import { TreeNode, TreeNodeConstructorType } from '../model/node/TreeNode';
import { asyncReadFile } from '../utils/asyncReadFile';
import { showFileError } from '../utils/showError';
import FileNotSelected from './common/FileNotSelected';

const TreeDisplay = <T extends TreeNodeConstructorType>(props: { treeFile: File | null; NodeClass: T }) => {
	const [treeRoot, setTreeRoot] = useState<TreeNode | null>(null);
	const [minSupport, setMinSupport] = useState<number>(0);

	const onFileRead = (content: string) => {
		let treeRootObj: any = null;
		try {
			treeRootObj = JSON.parse(content);
		} catch (e) {
			showFileError('Could not parse tree file');
			setTreeRoot(null);
			return;
		}

		try {
			if (typeof treeRootObj?.min_support !== 'number')
				throw new Error('Invalid tree file format: min_support missing or is not a number');

			const newTreeRoot: TreeNode = TreeNode.fromJson(treeRootObj?.tree, props.NodeClass);

			setMinSupport(treeRootObj.min_support);
			setTreeRoot(newTreeRoot);
		} catch (e: any) {
			showFileError(e?.message ?? 'Could not parse tree file');
			setTreeRoot(null);
		}
	};

	useEffect(() => {
		if (props.treeFile) asyncReadFile(props.treeFile, onFileRead);
	}, [props.treeFile]);

	return (
		<div style={{ width: '100%', height: '100%' }}>
			{treeRoot && (
				<Tree
					data={treeRoot}
					nodeSize={{ x: 300, y: 150 }}
					renderCustomNodeElement={(rd3tProps: CustomNodeElementProps) => {
						return renderNode({
							...rd3tProps,
							nodeDatum: rd3tProps.nodeDatum as unknown as TreeNode,
						});
					}}
				/>
			)}
			{!treeRoot && <FileNotSelected />}
		</div>
	);
};

const renderNode = ({ nodeDatum }: { nodeDatum: TreeNode }) => {
	return (
		<g>
			<circle r={15}></circle>
			<foreignObject width={250} height={100} x={-125} y={20}>
				<div
					style={{
						border: '1px solid black',
						backgroundColor: '#dededebe',
						padding: '0.1rem',
						width: '100%',
						height: '100%',
						display: 'flex',
						flexDirection: 'column',
					}}
				>
					<div style={{ textAlign: 'center' }}>
						<b>{joinListOrEmpty(nodeDatum.tokens)}</b>
					</div>
					<div style={{ fontSize: '0.8rem', overflowY: 'auto' }}>
						<div>
							<span>
								Support: <b>{nodeDatum.support}</b>
							</span>
							<span style={{ float: 'right' }}>
								{nodeDatum.idSetLabel} len: <b>{nodeDatum.idSet.length}</b>
							</span>
						</div>
						<p>
							Token ids: <b>{joinListOrEmpty(nodeDatum.tokensIds)}</b>
						</p>
						<p style={{ textAlign: 'center' }}>{nodeDatum.idSetLabel}:</p>
						<div>{joinListOrEmpty(nodeDatum.idSet)}</div>
					</div>
				</div>
			</foreignObject>
		</g>
	);
};

function joinListOrEmpty(list: Array<string | number>) {
	return list.length > 0 ? list.join(', ') : 'Φ';
}

export default TreeDisplay;
