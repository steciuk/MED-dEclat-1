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
    data: dict[int, list[int]], all_tokens_ids: set[int]
) -> dict[int, set[int]]:
    dif_map: dict[int, set[int]] = defaultdict(set)
    for transaction_id, tokens_ids in data.items():
        non_existing_tokens_ids: set[int] = all_tokens_ids - set(tokens_ids)
        for token_id in non_existing_tokens_ids:
            dif_map[token_id].add(transaction_id)

    return dict(dif_map)


class DeclatNode:
    def __init__(self, tokens_ids: list[int], support: int, dif_set: set[int]) -> None:
        self.tokens_ids: list[int] = tokens_ids
        self.tokens: list[str] = []
        self.support: int = support
        self.dif_set: set[int] = dif_set
        self.children: list[DeclatNode] = []

    def __repr__(self, layer=0) -> str:
        repr: str = "  " * layer
        repr += f"{self.support} - {self.tokens if len(self.tokens) > 0 else self.tokens_ids}\n"
        for child in self.children:
            repr += f"{child.__repr__(layer + 1)}"

        return repr

    def __str__(self) -> str:
        return self.__repr__()

    def add_child(self, child: "DeclatNode") -> None:
        self.children.append(child)

    def decode(self, tokens_map: dict[int, str]) -> None:
        self.tokens = [tokens_map[token_id] for token_id in self.tokens_ids]
        for child in self.children:
            child.decode(tokens_map)


def build_declat_root(
    dif_sets_map: dict[int, set[int]], num_transactions: int, min_support: int
) -> DeclatNode:
    declat_tree: DeclatNode = DeclatNode([], num_transactions, set())

    for token_id, dif_list in dif_sets_map.items():
        node_support: int = num_transactions - len(dif_list)
        if node_support > min_support:
            declat_tree.add_child(DeclatNode([token_id], node_support, dif_list))

    return declat_tree


def build_declat_tree(layer: list[DeclatNode], min_support) -> None:
    if len(layer) == 0:
        return

    new_layer: list[DeclatNode] = []

    for i, node in enumerate(layer):
        for other_node in layer[i + 1 :]:
            if node.tokens_ids[:-1] == other_node.tokens_ids[:-1]:
                new_dif_set: set[int] = other_node.dif_set - node.dif_set
                new_support: int = node.support - len(new_dif_set)
                if new_support > min_support:
                    new_node: DeclatNode = DeclatNode(
                        node.tokens_ids + [other_node.tokens_ids[-1]],
                        new_support,
                        new_dif_set,
                    )
                    node.add_child(new_node)
                    new_layer.append(new_node)

    build_declat_tree(new_layer, min_support)


def declat(directory: str, min_support: int) -> None:
    data_df, tokens_map_df = load_data(directory)

    validate_tokens_map(tokens_map_df)
    tokens_map: dict[int, str] = {
        token_id: row["token"] for token_id, row in tokens_map_df.iterrows()
    }
    all_tokens_ids: set[int] = set(tokens_map.keys())

    validate_data(data_df, all_tokens_ids)
    data: dict[int, list[int]] = {
        transaction_id: row["tokens"] for transaction_id, row in data_df.iterrows()
    }

    dif_sets_map: dict[int, set[int]] = get_dif_sets_map(data, all_tokens_ids)
    num_transactions: int = len(data)

    declat_tree: DeclatNode = build_declat_root(
        dif_sets_map, num_transactions, min_support
    )

    build_declat_tree(declat_tree.children, min_support)
    declat_tree.decode(tokens_map)
    print(declat_tree)


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
def declat_cli(directory: str, support: int) -> None:
    declat(directory, support)


if __name__ == "__main__":
    declat_cli()