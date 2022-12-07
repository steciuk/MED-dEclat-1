import React, { useEffect, useState } from 'react';

import FilePicker from './components/common/FilePicker';
import Rozette from './components/common/Rozette';
import MetadataDisplay from './components/MetadataDisplay';

const Application = () => {
	const [files, setFiles] = useState<File[]>([]);

	const [dataFile, setDataFile] = useState<File | null>(null);
	const [tokensMapFile, setTokensMapFile] = useState<File | null>(null);
	const [metadataFile, setMetadataFile] = useState<File | null>(null);
	const [declatTreeFile, setDeclatTreeFile] = useState<File | null>(null);

	const handleFilesChange = (files: File[]) => {
		console.log(files);
		setFiles(files);
	};

	useEffect(() => {
		let metadataFile: File | null = null;
		let declatTreeFile: File | null = null;
		let dataFile: File | null = null;
		let tokensMapFile: File | null = null;

		files.some((file: File) => {
			switch (file.name) {
				case 'metadata.json':
					metadataFile = file;
					break;
				case 'declat-tree.json':
					declatTreeFile = file;
					break;
				case 'data.json':
					dataFile = file;
					break;
				case 'tokens-map.json':
					tokensMapFile = file;
					break;
			}

			return metadataFile && declatTreeFile && dataFile && tokensMapFile;
		});

		setDataFile(dataFile);
		setTokensMapFile(tokensMapFile);
		setMetadataFile(metadataFile);
		setDeclatTreeFile(declatTreeFile);
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
				<Rozette title="Tokens map">Hello</Rozette>
				<Rozette title="Data">Hello</Rozette>
				<Rozette title="Declat tree">Hello</Rozette>
			</div>
		</div>
	);
};

export default Application;
