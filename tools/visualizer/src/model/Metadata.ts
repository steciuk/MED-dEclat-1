import { enumHasValue } from '../utils/enumHasValue';

export class Metadata {
	constructor(
		public readonly subreddit: string,
		public readonly listing: Listing,
		public readonly numPosts: number,
		public readonly timeFilter?: TimeFilter
	) {}

	static fromJson(json: any): Metadata {
		if (typeof json !== 'object' || json === null) throw new Error('Invalid metadata file');
		if (typeof json?.subreddit !== 'string')
			throw new Error('Invalid metadata file format: subreddit missing or is not a string');
		if (!('listing' in json) || !enumHasValue(Listing, json.listing))
			throw new Error('Invalid metadata file format: listing missing or is not a valid listing');
		if (typeof json?.num_posts !== 'number')
			throw new Error('Invalid metadata file format: num_posts missing or is not a number');

		let timeFilter: TimeFilter | undefined;
		if (json.listing === Listing.TOP || json.listing === Listing.CONTROVERSIAL) {
			if (!('time_filter' in json) || !enumHasValue(TimeFilter, json.time_filter))
				throw new Error('Invalid metadata file format: time_filter missing or is not a valid time filter');
			timeFilter = json.time_filter;
		}

		return new Metadata(json.subreddit, json.listing, json.num_posts, timeFilter);
	}
}

export enum Listing {
	HOT = 'hot',
	NEW = 'new',
	TOP = 'top',
	CONTROVERSIAL = 'controversial',
}

export enum TimeFilter {
	ALL = 'all',
	YEAR = 'year',
	MONTH = 'month',
	WEEK = 'week',
	DAY = 'day',
}
