import re
from datetime import datetime
from typing import Literal, Union

import click
import nltk
import pandas as pd
import praw

from reddit_secrets import CLIENT_ID, CLIENT_SECRET

Listing = Union[
    Literal["hot"], Literal["new"], Literal["top"], Literal["controversial"]
]

Time_filter = Union[
    Literal["day"],
    Literal["week"],
    Literal["month"],
    Literal["year"],
    Literal["all"],
]


def stem(stemmer: nltk.stem.PorterStemmer, title: str) -> list[str]:
    word_tokens = nltk.tokenize.word_tokenize(title)
    return [stemmer.stem(w) for w in word_tokens]


@click.command()
@click.option("-s", "--subreddit", required=True, help="Subreddit to scrape")
@click.option(
    "-n",
    "--num_posts",
    default=100,
    show_default=True,
    type=click.IntRange(min=1),
    help="Number of posts to scrape",
)
@click.option(
    "-l",
    "--listing",
    default="top",
    show_default=True,
    type=click.Choice(["hot", "new", "top", "controversial"]),
    help="Listing to use",
)
@click.option(
    "-t",
    "--time_filter",
    default="all",
    show_default=True,
    type=click.Choice(["day", "week", "month", "year", "all"]),
    help="Time filter. Used only for top and controversial",
)
@click.option(
    "-d",
    "--directory",
    default="data",
    show_default=True,
    type=click.Path(exists=True),
    help="Directory to save the data",
)
def get_reddit_data(
    subreddit: str,
    num_posts: int,
    listing: Listing,
    time_filter: Time_filter,
    directory: str,
) -> None:
    reddit = praw.Reddit(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent="EitiMed"
    )
    subreddit = subreddit.lower()

    # get posts
    sub = reddit.subreddit(subreddit)
    posts = []
    if listing == "hot":
        posts = sub.hot(limit=num_posts)
    elif listing == "new":
        posts = sub.new(limit=num_posts)
    elif listing == "top":
        posts = sub.top(limit=num_posts, time_filter=time_filter)
    elif listing == "controversial":
        posts = sub.controversial(limit=num_posts, time_filter=time_filter)
    else:
        print("Invalid listing type")

    # create dataframe
    df = pd.DataFrame([post.title for post in posts], columns=["title"])

    # remove all non-alpha characters
    df["title"] = df["title"].apply(lambda x: re.sub("[^a-zA-Z\s]", "", x))

    # stem words
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

    ps = nltk.stem.PorterStemmer()
    df["stemmed"] = df["title"].apply(lambda x: stem(ps, x))

    # save to json
    file_path = f"{directory}/{subreddit}_{num_posts}_{listing}"
    if listing in ["top", "controversial"]:
        file_path += f"_{time_filter}"

    time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path += f"_{time}.json"

    df.to_json(file_path, indent=2)


if __name__ == "__main__":
    get_reddit_data()
