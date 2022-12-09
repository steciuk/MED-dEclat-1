import json
import re
from datetime import datetime
from pathlib import Path
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


def remove_non_alpha(series: "pd.Series[str]") -> "pd.Series[str]":
    return series.apply(lambda x: re.sub(r"[^a-zA-Z\s]", "", x))


def remove_duplicates_in_rows(series: "pd.Series[list[str]]") -> "pd.Series[list[str]]":
    return series.apply(lambda x: list(dict.fromkeys(x)))


def create_token_ids(
    series: "pd.Series[list[str]]",
) -> tuple["pd.Series[list[int]]", dict[str, int]]:
    tokens_map: dict[str, int] = {}
    token_ids: dict[int, list[int]] = {}

    for i, tokens in series.items():
        row_token_ids: list[int] = []
        for token in tokens:
            token_id: int | None = tokens_map.get(token)
            if token_id is None:
                token_id = len(tokens_map)
                row_token_ids.append(token_id)
                tokens_map[token] = token_id
            else:
                row_token_ids.append(token_id)

        token_ids[i] = row_token_ids

    return pd.Series(token_ids, dtype=object), tokens_map


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
    type=click.Path(),
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
    sub = reddit.subreddit(subreddit)

    print("Getting data from Reddit...")
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

    posts = list(posts)
    if len(posts) < num_posts:
        print(f"WARNING: Only {len(posts)} posts found")
        num_posts = len(posts)

    data_df = pd.DataFrame(
        [[post.title, None] for post in posts], columns=["title", "tokens"]
    )

    print("Removing non-alphabetic characters...")
    titles: pd.Series[str] = remove_non_alpha(data_df["title"])

    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

    print("Stemming titles...")
    ps = nltk.stem.PorterStemmer()
    stemmed_titles: "pd.Series[list[str]]" = titles.apply(lambda x: stem(ps, x))

    print("Removing duplicated tokens...")
    stemmed_titles = remove_duplicates_in_rows(stemmed_titles)

    print("Creating token ids...")
    data_df["tokens"], tokens_map = create_token_ids(stemmed_titles)
    tokens_map_df = pd.DataFrame(
        list(tokens_map.items()), columns=["token", "token_id"]
    ).set_index("token_id")

    print("Saving data...")
    output_dir = f"{directory}/{subreddit}_{num_posts}_{listing}"
    if listing in ["top", "controversial"]:
        output_dir += f"_{time_filter}"

    time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir += f"_{time}"

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    data_df.to_json(f"{output_dir}/data.json", indent=2)
    tokens_map_df.to_json(f"{output_dir}/tokens_map.json", indent=2)

    with open(f"{output_dir}/metadata.json", "w") as file:
        json.dump(
            {
                "subreddit": subreddit,
                "listing": listing,
                "time_filter": time_filter,
                "num_posts": num_posts,
            },
            file,
            indent=2,
        )

    print(f"All good! Data saved to {output_dir}")


if __name__ == "__main__":
    get_reddit_data()
