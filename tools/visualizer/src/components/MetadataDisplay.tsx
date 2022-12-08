import React, { useEffect, useState } from 'react';

import { Button } from '@mui/material';

import { Listing, Metadata, TimeFilter } from '../model/Metadata';
import { asyncReadFile } from '../utils/asyncReadFile';
import { enumHasValue } from '../utils/enumHasValue';
import { showFileError } from '../utils/showError';

const MetadataDisplay = (props: { metadataFile: File | null }) => {
	const [metadata, setMetadata] = useState<Metadata | null>(null);

	const onFileRead = (content: string) => {
		let newMetadata: any = null;
		try {
			newMetadata = JSON.parse(content);
		} catch (e) {
			showFileError('Could not parse metadata.json');
			setMetadata(null);
			return;
		}

		try {
			if (validateMetadata(newMetadata)) {
				setMetadata(newMetadata);
			} else {
				showFileError('Could not parse metadata.json');
				setMetadata(null);
			}
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

function validateMetadata(metadata: any): metadata is Metadata {
	if (typeof metadata !== 'object' || metadata === null) throw new Error('Invalid metadata.json file format');
	if (typeof metadata?.subreddit !== 'string')
		throw new Error('Invalid metadata: subreddit missing or is not a string');
	if (!('listing' in metadata) || !enumHasValue(Listing, metadata.listing))
		throw new Error('Invalid metadata: listing missing or is not a valid listing');
	if (typeof metadata?.num_posts !== 'number')
		throw new Error('Invalid metadata: num_posts missing or is not a number');

	metadata.numPosts = metadata.num_posts;
	delete metadata.num_posts;

	if (metadata.listing === Listing.TOP || metadata.listing === Listing.CONTROVERSIAL) {
		if (!('time_filter' in metadata) || !enumHasValue(TimeFilter, metadata.time_filter))
			throw new Error('Invalid metadata: time_filter missing or is not a valid time filter');
		metadata.timeFilter = metadata.time_filter;
		delete metadata.time_filter;
	}

	return true;
}

export default MetadataDisplay;
