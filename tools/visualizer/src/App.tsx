import { useState } from 'react';

import FilePicker from './components/FilePicker';

function App() {
	const [dataFile, setDataFile] = useState<File | null>(null);
	const [tokensMapFile, setTokensMapFile] = useState<File | null>(null);
	const [metadataFile, setMetadataFile] = useState<File | null>(null);
	const [declatTreeFile, setDeclatTreeFile] = useState<File | null>(null);

	const handleDataFileChange = (file: File) => {
		setDataFile(file);
	};
	const handleTokensMapFileChange = (file: File) => {
		setTokensMapFile(file);
	};
	const handleMetadataFileChange = (file: File) => {
		setMetadataFile(file);
	};
	const handleDeclatTreeFileChange = (file: File) => {
		setDeclatTreeFile(file);
	};

	return (
		<div>
			<FilePicker
				handleDataFileChange={handleDataFileChange}
				handleTokensMapFileChange={handleTokensMapFileChange}
				handleMetadataFileChange={handleMetadataFileChange}
				handleDeclatTreeFileChange={handleDeclatTreeFileChange}
			/>
		</div>
	);
}

export default App;
