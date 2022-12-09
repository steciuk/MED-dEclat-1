import React, { useEffect, useState } from 'react';

import { Button } from '@mui/material';

import { Metadata } from '../model/Metadata';
import { asyncReadFile } from '../utils/asyncReadFile';
import { showFileError } from '../utils/showError';

const MetadataDisplay = (props: { metadataFile: File | null }) => {
	const [metadata, setMetadata] = useState<Metadata | null>(null);

	const onFileRead = (content: string) => {
		let metadataObj: any = null;
		try {
			metadataObj = JSON.parse(content);
		} catch (e) {
			showFileError('Could not parse metadata.json');
			setMetadata(null);
			return;
		}

		try {
			const newMetadata = Metadata.fromJson(metadataObj);
			setMetadata(newMetadata);
		} catch (e: any) {
			showFileError(e?.message ?? 'Could not parse metadata.json');
			setMetadata(null);
		}
	};

	useEffect(() => {
		if (props.metadataFile) asyncReadFile(props.metadataFile, onFileRead);
	}, [props.metadataFile]);

	return (
		<div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
			{metadata && (
				<>
					<div style={{ display: 'flex', gap: '2rem' }}>
						<div>
							Subreddit: <strong>{metadata.subreddit}</strong>
						</div>
						<div>
							Listing: <strong>{metadata.listing}</strong>
						</div>
						{metadata.timeFilter && (
							<div>
								Time filter: <strong>{metadata.timeFilter}</strong>
							</div>
						)}
						<div>
							Number of posts: <strong>{metadata.numPosts}</strong>
						</div>
					</div>
					<Button
						size="small"
						onClick={() => window.open(`https://www.reddit.com/r/${metadata.subreddit}/${metadata.listing}`)}
					>
						Go to subreddit
					</Button>
				</>
			)}
			{!metadata && <div>No metadata.json file selected</div>}
		</div>
	);
};

export default MetadataDisplay;
