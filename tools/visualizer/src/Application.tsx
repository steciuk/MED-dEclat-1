import React, { useEffect, useState } from 'react';

import FilePicker from './components/common/FilePicker';
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
		<div style={{ backgroundColor: 'lightgray', height: '100vh' }}>
			<div style={{ display: 'flex', justifyContent: 'space-between', padding: '1rem' }}>
				<FilePicker handleFilesChange={handleFilesChange} />
				<MetadataDisplay metadataFile={metadataFile} />
			</div>
		</div>
	);
};

export default Application;
