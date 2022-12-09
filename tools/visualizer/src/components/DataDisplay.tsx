import { AgGridReact } from 'ag-grid-react';
import React, { useEffect, useState } from 'react';

import { DataEntry } from '../model/DataEntry';
import { asyncReadFile } from '../utils/asyncReadFile';
import { showFileError } from '../utils/showError';
import FileNotSelected from './common/FileNotSelected';

const DataDisplay = (props: { dataFile: File | null }) => {
	const [data, setData] = useState<DataEntry[] | null>(null);

	const onFileRead = (content: string) => {
		let newDataObj: any = null;

		try {
			newDataObj = JSON.parse(content);
		} catch (e) {
			showFileError('Could not parse data.json');
			setData(null);
			return;
		}

		if (typeof newDataObj !== 'object' || newDataObj === null) {
			showFileError('Could not parse data.json');
			setData(null);
			return;
		}

		try {
			if (typeof newDataObj?.title !== 'object' || newDataObj?.title === null)
				throw new Error('Invalid data file format');

			const newData = Object.values(newDataObj.title).map((value: unknown, index: number) => {
				return DataEntry.fromJson({ title: value, tokens: newDataObj?.tokens?.[index] });
			});

			setData(newData);
		} catch (e: any) {
			showFileError(e?.message ?? 'Could not parse data.json');
			setData(null);
		}
	};

	useEffect(() => {
		if (props.dataFile) asyncReadFile(props.dataFile, onFileRead);
	}, [props.dataFile]);

	return (
		<div style={{ width: '100%', height: '100%' }}>
			{data && (
				<div className="ag-theme-alpine" style={{ width: '100%', height: '100%' }}>
					<AgGridReact
						rowData={data.map((entry) => {
							return { title: entry.title, tokens: entry.tokens };
						})}
						columnDefs={[
							{ field: 'title', headerName: 'Title' },
							{ field: 'tokens', headerName: 'Tokens' },
						]}
						defaultColDef={{ sortable: true, filter: true, flex: 1 }}
					/>
				</div>
			)}
			{!data && <FileNotSelected />}
		</div>
	);
};

export default DataDisplay;
