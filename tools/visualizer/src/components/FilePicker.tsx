import React, { useRef } from 'react';

import { Button } from '@mui/material';

const FilePicker = (props: {
	handleDataFileChange: (file: File) => void;
	handleTokensMapFileChange: (file: File) => void;
	handleMetadataFileChange: (file: File) => void;
	handleDeclatTreeFileChange: (file: File) => void;
}) => {
	const fileInputRef = useRef<HTMLInputElement>(null);

	const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		if (!event.target.files) return;

		const files: File[] = Object.values(event.target.files);

		let metadataFile: File | null = null;
		let declatTreeFile: File | null = null;
		let dataFile: File | null = null;
		let tokensMapFile: File | null = null;

		files.some((file) => {
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

		if (metadataFile) props.handleMetadataFileChange(metadataFile);
		if (declatTreeFile) props.handleDeclatTreeFileChange(declatTreeFile);
		if (dataFile) props.handleDataFileChange(dataFile);
		if (tokensMapFile) props.handleTokensMapFileChange(tokensMapFile);
	};

	return (
		<div>
			<Button variant={'contained'} onClick={() => fileInputRef.current?.click()}>
				Upload files
			</Button>

			<input
				style={{ display: 'none' }}
				ref={fileInputRef}
				type="file"
				onChange={handleFileChange}
				multiple={true}
			/>
		</div>
	);
};

export default FilePicker;
