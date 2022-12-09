import json
from typing import Literal, Union

import click
import pandas as pd

Algorithm = Union[Literal["eclat"], Literal["declat"]]


class TreeNode:
    def __init__(self, tokens_ids: list[int], support: int, id_set: set[int]) -> None:
        self.tokens_ids: list[int] = tokens_ids
        self.tokens: list[str] = []
        self.support: int = support
        self.id_set: set[int] = id_set
        self.children: list[TreeNode] = []

    def __repr__(self, layer=0) -> str:
        repr: str = "  " * layer
        repr += f"{self.support} - {self.tokens if len(self.tokens) > 0 else self.tokens_ids}\n"
        for child in self.children:
            repr += f"{child.__repr__(layer + 1)}"

        return repr

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TreeNode):
            return False

        return (
            self.tokens_ids == other.tokens_ids
            and self.support == other.support
            and self.id_set == other.id_set
        )

    def add_child(self, child: "TreeNode") -> None:
        self.children.append(child)

    def decode(self, tokens_map: dict[int, str]) -> None:
        self.tokens = [tokens_map[token_id] for token_id in self.tokens_ids]
        for child in self.children:
            child.decode(tokens_map)


class TreeJSONEncoder(json.JSONEncoder):
    def default(self, o: object) -> object:
        if isinstance(o, TreeNode):
            return o.__dict__
        if isinstance(o, set):
            return list(o)

        return json.JSONEncoder.default(self, o)


def load_data(directory: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    try:
        tokens_map_df: pd.DataFrame = pd.read_json(
            f"{directory}/tokens_map.json"
        ).sort_index()
    except FileNotFoundError:
        raise FileNotFoundError("No tokens_map.json file found in the directory")

    try:
        data_df: pd.DataFrame = pd.read_json(f"{directory}/data.json").sort_index()
        return data_df, tokens_map_df
    except FileNotFoundError:
        print("No data.json file found in the directory")
        raise FileNotFoundError("No data.json file found in the directory")


def validate_data(data_df: pd.DataFrame, all_tokens_ids: set[int]) -> None:
    if "tokens" not in data_df.columns:
        raise ValueError("No tokens column found in data.json")

    if not all(isinstance(tokens, list) for tokens in data_df["tokens"]):
        raise ValueError("Values in tokens column are not lists")

    for tokens in data_df["tokens"]:
        for token in tokens:
            if token not in all_tokens_ids:
                raise ValueError(f"Token {token} not found in tokens_map.json")


def validate_tokens_map(tokens_map_df: pd.DataFrame) -> None:
    if "token" not in tokens_map_df.columns:
        raise ValueError("No token column found in tokens_map.json")

    if not all(isinstance(token, str) for token in tokens_map_df["token"]):
        raise ValueError("Values in token column are not strings")

    if len(tokens_map_df["token"]) != len(set(tokens_map_df["token"])):
        raise ValueError("Duplicate tokens found in tokens_map.json")

    if len(tokens_map_df.index) != len(set(tokens_map_df.index)):
        raise ValueError("Duplicate tokens ids found in tokens_map.json")


# DECLAT
def get_dif_sets_map(
    data: dict[int, list[int]], all_tokens_ids: set[int]
) -> dict[int, set[int]]:
    dif_map: dict[int, set[int]] = {token_id: set() for token_id in all_tokens_ids}
    for transaction_id, tokens_ids in data.items():
        non_existing_tokens_ids: set[int] = all_tokens_ids - set(tokens_ids)
        for token_id in non_existing_tokens_ids:
            dif_map[token_id].add(transaction_id)

    return dif_map


def build_declat_root(
    id_sets_map: dict[int, set[int]], num_transactions: int, min_support: int
) -> TreeNode:
    declat_tree: TreeNode = TreeNode([], num_transactions, set())

    for token_id, dif_list in id_sets_map.items():
        node_support: int = num_transactions - len(dif_list)
        if node_support > min_support:
            declat_tree.add_child(TreeNode([token_id], node_support, dif_list))

    return declat_tree


def build_declat_tree(layer: list[TreeNode], min_support) -> None:
    if len(layer) == 0:
        return

    new_layer: list[TreeNode] = []

    for i, node in enumerate(layer):
        for other_node in layer[i + 1 :]:
            if node.tokens_ids[:-1] == other_node.tokens_ids[:-1]:
                new_id_set: set[int] = other_node.id_set - node.id_set
                new_support: int = node.support - len(new_id_set)
                if new_support > min_support:
                    new_node: TreeNode = TreeNode(
                        node.tokens_ids + [other_node.tokens_ids[-1]],
                        new_support,
                        new_id_set,
                    )
                    node.add_child(new_node)
                    new_layer.append(new_node)

    build_declat_tree(new_layer, min_support)


# ECLAT
def get_tid_sets_map(
    data: dict[int, list[int]], all_tokens_ids: set[int]
) -> dict[int, set[int]]:
    tid_map: dict[int, set[int]] = {token_id: set() for token_id in all_tokens_ids}
    for transaction_id, tokens_ids in data.items():
        for token_id in tokens_ids:
            tid_map[token_id].add(transaction_id)

    return tid_map


def build_eclat_root(
    id_sets_map: dict[int, set[int]],
    num_transactions: int,
    min_support: int,
    all_tokens_ids: set[int],
) -> TreeNode:
    eclat_tree: TreeNode = TreeNode([], num_transactions, all_tokens_ids)

    for token_id, tid_list in id_sets_map.items():
        node_support: int = len(tid_list)
        if node_support > min_support:
            eclat_tree.add_child(TreeNode([token_id], node_support, tid_list))

    return eclat_tree


def build_eclat_tree(layer: list[TreeNode], min_support) -> None:
    if len(layer) == 0:
        return

    new_layer: list[TreeNode] = []

    for i, node in enumerate(layer):
        for other_node in layer[i + 1 :]:
            if node.tokens_ids[:-1] == other_node.tokens_ids[:-1]:
                new_id_set: set[int] = node.id_set & other_node.id_set
                new_support: int = len(new_id_set)
                if new_support > min_support:
                    new_node: TreeNode = TreeNode(
                        node.tokens_ids + [other_node.tokens_ids[-1]],
                        new_support,
                        new_id_set,
                    )
                    node.add_child(new_node)
                    new_layer.append(new_node)

    build_eclat_tree(new_layer, min_support)


def save_tree(
    declat_tree: TreeNode, directory: str, min_support: int, algorithm: Algorithm
) -> None:
    result = {"min_support": min_support, "tree": declat_tree}
    with open(f"{directory}/{algorithm}.json", "w") as file:
        json.dump(result, file, indent=2, cls=TreeJSONEncoder)


def build_tree(directory: str, min_support: int, algorithm: Algorithm) -> None:
    print("Reading data...")
    data_df, tokens_map_df = load_data(directory)

    print("Validating tokens_map.json...")
    validate_tokens_map(tokens_map_df)
    tokens_map: dict[int, str] = {
        token_id: row["token"] for token_id, row in tokens_map_df.iterrows()
    }
    all_tokens_ids: set[int] = set(tokens_map.keys())

    print("Validating data.json...")
    validate_data(data_df, all_tokens_ids)
    data: dict[int, list[int]] = {
        transaction_id: row["tokens"] for transaction_id, row in data_df.iterrows()
    }

    num_transactions: int = len(data)
    tree: Union[TreeNode, None] = None

    if algorithm == "declat":
        print("Creating dif-sets...")
        dif_sets_map: dict[int, set[int]] = get_dif_sets_map(data, all_tokens_ids)

        print(f"Building {algorithm} root...")
        tree = build_declat_root(dif_sets_map, num_transactions, min_support)

        print(f"Building {algorithm} tree...")
        build_declat_tree(tree.children, min_support)
    elif algorithm == "eclat":
        print("Creating tid-sets...")
        tid_sets_map: dict[int, set[int]] = get_tid_sets_map(data, all_tokens_ids)

        print(f"Building {algorithm} root...")
        tree = build_eclat_root(
            tid_sets_map, num_transactions, min_support, all_tokens_ids
        )

        print(f"Building {algorithm} tree...")
        build_eclat_tree(tree.children, min_support)
    else:
        raise ValueError(f"Unknown algorithm {algorithm}")

    print("Decoding tokens...")
    tree.decode(tokens_map)

    print(f"Saving {algorithm} tree...")
    save_tree(tree, directory, min_support, algorithm)

    print(f"All good! Declat tree saved to {directory}/{algorithm}.json")


@click.command()
@click.option(
    "-d",
    "--directory",
    required=True,
    type=click.Path(exists=True),
    help="Directory to load the data from",
)
@click.option(
    "-s",
    "--support",
    required=True,
    type=click.IntRange(min=1),
    help="Minimum support for frequent itemsets",
)
@click.option(
    "-a",
    "--algorithm",
    default="declat",
    show_default=True,
    type=click.Choice(["declat", "eclat"]),
    help="Algorithm to run",
)
def build_tree_cli(directory: str, support: int, algorithm: Algorithm) -> None:
    build_tree(directory, support, algorithm)


if __name__ == "__main__":
    build_tree_cli()
