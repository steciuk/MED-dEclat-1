from collections import defaultdict

import click
import pandas as pd


def load_data(directory: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    try:
        tokens_map_df: pd.DataFrame = pd.read_json(
            f"{directory}/tokens_map.json"
        ).sort_index()
    except FileNotFoundError:
        print("No tokens_map.json file found in the directory")
        exit(1)

    try:
        data_df: pd.DataFrame = pd.read_json(f"{directory}/data.json").sort_index()
        return data_df, tokens_map_df
    except FileNotFoundError:
        print("No data.json file found in the directory")
        exit(1)


def validate_data(data_df: pd.DataFrame, all_tokens_ids: set[int]) -> None:
    if "tokens" not in data_df.columns:
        print("No tokens column found in data.json")
        exit(1)

    if not all(isinstance(tokens, list) for tokens in data_df["tokens"]):
        print("Values in tokens column are not lists")
        exit(1)

    for tokens in data_df["tokens"]:
        for token in tokens:
            if token not in all_tokens_ids:
                print(f"Token {token} not found in tokens_map.json")
                exit(1)


def validate_tokens_map(tokens_map_df: pd.DataFrame) -> None:
    if "token" not in tokens_map_df.columns:
        print("No token column found in tokens_map.json")
        exit(1)

    if not all(isinstance(token, str) for token in tokens_map_df["token"]):
        print("Values in token column are not strings")
        exit(1)


def get_dif_sets_map(
    data_df: pd.DataFrame, all_tokens_ids: set[int]
) -> dict[int, set[int]]:
    dif_map: dict[int, set[int]] = defaultdict(set)
    for transaction_id, row in data_df.iterrows():
        non_existing_tokens_ids: set[int] = all_tokens_ids - set(row["tokens"])
        for token_id in non_existing_tokens_ids:
            dif_map[token_id].add(transaction_id)

    return dict(dif_map)


@click.command()
@click.option(
    "-d",
    "--directory",
    type=click.Path(exists=True),
    help="Directory to load the data from",
)
@click.option(
    "-s",
    "--support",
    type=click.IntRange(min=1),
    default=2,
    show_default=True,
    help="Minimum support for frequent itemsets",
)
def declat(directory: str, support: int) -> None:
    data_df, tokens_map_df = load_data(directory)

    validate_tokens_map(tokens_map_df)
    all_tokens_ids: set[int] = set(tokens_map_df.index)
    validate_data(data_df, all_tokens_ids)

    dif_sets_map: dict[int, set[int]] = get_dif_sets_map(data_df, all_tokens_ids)

    num_transactions: int = len(data_df)


if __name__ == "__main__":
    declat()
