export function asyncReadFile(file: File, onFileRead: (content: string) => void) {
	const reader = new FileReader();
	reader.onloadend = () => {
		if (reader.result) {
			onFileRead(reader.result as string);
		}
	};

	reader.readAsText(file);
}
