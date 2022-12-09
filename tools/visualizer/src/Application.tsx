import React, { useEffect, useState } from 'react';

import FilePicker from './components/common/FilePicker';
import Rozette from './components/common/Rozette';
import DataDisplay from './components/DataDisplay';
import MetadataDisplay from './components/MetadataDisplay';
import TokenMapDisplay from './components/TokenMapDisplay';
import TreeDisplay from './components/TreeDisplay';
import { DeclatNode } from './model/node/DeclatNode';
import { EclatNode } from './model/node/EclatNode';

const Application = () => {
	const [files, setFiles] = useState<File[]>([]);

	const [dataFile, setDataFile] = useState<File | null>(null);
	const [tokensMapFile, setTokensMapFile] = useState<File | null>(null);
	const [metadataFile, setMetadataFile] = useState<File | null>(null);
	const [declatTreeFile, setDeclatTreeFile] = useState<File | null>(null);
	const [eclatTreeFile, setEclatTreeFile] = useState<File | null>(null);

	const handleFilesChange = (files: File[]) => {
		setFiles(files);
	};

	useEffect(() => {
		let metadataFile: File | null = null;
		let declatTreeFile: File | null = null;
		let eclatTreeFile: File | null = null;
		let dataFile: File | null = null;
		let tokensMapFile: File | null = null;

		files.some((file: File) => {
			switch (file.name) {
				case 'metadata.json':
					metadataFile = file;
					break;
				case 'declat.json':
					declatTreeFile = file;
					break;
				case 'eclat.json':
					eclatTreeFile = file;
					break;
				case 'data.json':
					dataFile = file;
					break;
				case 'tokens_map.json':
					tokensMapFile = file;
					break;
			}

			return metadataFile && declatTreeFile && dataFile && tokensMapFile;
		});

		setDataFile(dataFile);
		setTokensMapFile(tokensMapFile);
		setMetadataFile(metadataFile);
		setDeclatTreeFile(declatTreeFile);
		setEclatTreeFile(eclatTreeFile);
	}, [files]);

	return (
		<div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
			<div style={{ display: 'flex', justifyContent: 'space-between', margin: '1rem' }}>
				<FilePicker handleFilesChange={handleFilesChange} />
				<MetadataDisplay metadataFile={metadataFile} />
			</div>
			<div
				style={{
					display: 'flex',
					margin: '0 1rem 1rem 1rem',
					flexGrow: '1',
					boxShadow: '8px 8px 24px 0px rgba(66, 68, 90, 1)',
				}}
			>
				<Rozette title="Tokens map" defaultHidden={true}>
					<TokenMapDisplay tokenMapFile={tokensMapFile} />
				</Rozette>
				<Rozette title="Data" defaultHidden={true}>
					<DataDisplay dataFile={dataFile} />
				</Rozette>
				<Rozette title="Declat tree">
					<TreeDisplay treeFile={declatTreeFile} NodeClass={DeclatNode} />
				</Rozette>
				<Rozette title="Eclat tree">
					<TreeDisplay treeFile={eclatTreeFile} NodeClass={EclatNode} />
				</Rozette>
			</div>
		</div>
	);
};

export default Application;
