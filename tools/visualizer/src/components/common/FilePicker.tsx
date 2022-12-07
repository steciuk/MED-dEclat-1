import React, { ChangeEvent, useRef } from 'react';

import { Button } from '@mui/material';

const FilePicker = (props: { handleFilesChange: (files: File[]) => void }) => {
	const fileInputRef = useRef<HTMLInputElement>(null);

	const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
		if (event.target.files) {
			props.handleFilesChange(Array.from(event.target.files));
			fileInputRef.current?.value && (fileInputRef.current.value = '');
		}
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
