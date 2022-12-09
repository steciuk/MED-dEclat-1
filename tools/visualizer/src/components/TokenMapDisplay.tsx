import { AgGridReact } from 'ag-grid-react';
import React, { useEffect, useState } from 'react';

import { TokensMapEntry } from '../model/TokensMapEntry';
import { asyncReadFile } from '../utils/asyncReadFile';
import { showFileError } from '../utils/showError';
import FileNotSelected from './common/FileNotSelected';

const TokenMapDisplay = (props: { tokenMapFile: File | null }) => {
	const [tokensMap, setTokenMap] = useState<TokensMapEntry[] | null>(null);

	const onFileRead = (content: string) => {
		let newTokenMapObj: any = null;
		try {
			newTokenMapObj = JSON.parse(content);
		} catch (e) {
			showFileError('Could not parse tokens_map.json');
			setTokenMap(null);
			return;
		}

		if (!(typeof newTokenMapObj === 'object') || newTokenMapObj === null) {
			showFileError('Could not parse tokens_map.json');
			setTokenMap(null);
			return;
		}

		try {
			if (typeof newTokenMapObj?.token !== 'object' || newTokenMapObj?.token === null)
				throw new Error('Invalid token map file format');

			const newTokensMap = Object.entries(newTokenMapObj.token).map(([key, value]: [unknown, unknown]) => {
				return TokensMapEntry.fromJson({ id: key, token: value });
			});

			setTokenMap(newTokensMap);
		} catch (e: any) {
			showFileError(e?.message ?? 'Could not parse tokens_map.json');
			setTokenMap(null);
		}
	};

	useEffect(() => {
		if (props.tokenMapFile) asyncReadFile(props.tokenMapFile, onFileRead);
	}, [props.tokenMapFile]);

	return (
		<div style={{ width: '100%', height: '100%' }}>
			{tokensMap && (
				<div className="ag-theme-alpine" style={{ width: '100%', height: '100%' }}>
					<AgGridReact
						rowData={tokensMap.map((entry) => {
							return { id: entry.id, token: entry.token };
						})}
						columnDefs={[
							{ field: 'id', headerName: 'Token id' },
							{ field: 'token', headerName: 'Token' },
						]}
						defaultColDef={{ sortable: true, filter: true, flex: 1 }}
					/>
				</div>
			)}
			{!tokensMap && <FileNotSelected />}
		</div>
	);
};

export default TokenMapDisplay;
