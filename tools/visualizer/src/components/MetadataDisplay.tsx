import React, { useEffect, useState } from 'react';

import { Button } from '@mui/material';

import { Listing, Metadata, TimeFilter } from '../model/Metadata';
import { asyncReadFile } from '../utils/asyncReadFile';
import { enumHasValue } from '../utils/enumHasValue';
import { showFileError } from '../utils/showError';

const MetadataDisplay = (props: { metadataFile: File | null }) => {
	const [metadata, setMetadata] = useState<Metadata | null>(null);

	const onFileRead = (content: string) => {
		let metadata: any = null;
		try {
			metadata = JSON.parse(content);
		} catch (e) {
			showFileError('metadata.json');
			setMetadata(null);
			return;
		}

		if (vadivdateMetadata(metadata)) {
			setMetadata(metadata);
		} else {
			showFileError('metadata.json');
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

function vadivdateMetadata(metadata: any): metadata is Metadata {
	if (typeof metadata !== 'object' || metadata === null) return false;
	if (!('subreddit' in metadata) || typeof metadata.subreddit !== 'string') return false;
	if (!('listing' in metadata) || !enumHasValue(Listing, metadata.listing)) return false;
	if (!('num_posts' in metadata) || typeof metadata.num_posts !== 'number') return false;

	metadata.numPosts = metadata.num_posts;
	delete metadata.num_posts;

	if (metadata.listing === Listing.TOP || metadata.listing === Listing.CONTROVERSIAL) {
		if (!('time_filter' in metadata) || !enumHasValue(TimeFilter, metadata.time_filter)) return false;
		metadata.timeFilter = metadata.time_filter;
		delete metadata.time_filter;
	}

	return true;
}

export default MetadataDisplay;
