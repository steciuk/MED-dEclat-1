export type Metadata = {
	subreddit: string;
	listing: Listing;
	numPosts: number;
	timeFilter?: TimeFilter;
};

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
