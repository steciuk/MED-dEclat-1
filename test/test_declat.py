import pandas as pd
import pytest

from declat import (
    DeclatNode,
    build_declat_root,
    build_declat_tree,
    get_dif_sets_map,
    load_data,
    validate_data,
    validate_tokens_map,
)


# load_data
def test_load_data_missing_files() -> None:
    with pytest.raises(FileNotFoundError) as e:
        load_data("test/test_declat_data/missing_data")

    assert str(e.value) == "No data.json file found in the directory"

    with pytest.raises(FileNotFoundError) as e:
        load_data("test/test_declat_data/missing_tokens_map")

    assert str(e.value) == "No tokens_map.json file found in the directory"


def test_load_data() -> None:
    data_df, tokens_map_df = load_data("test/test_declat_data/valid")

    assert data_df["tokens"].equals(pd.Series([[0, 1], [2, 3]]))
    assert tokens_map_df.equals(
        pd.DataFrame({"token": ["hello", "world", "hey", "welcome"]})
    )


# validate_data
def test_validate_data_no_tokens_column() -> None:
    data_df = pd.DataFrame({"not_tokens": [[0, 1], [2, 3]]})

    with pytest.raises(ValueError) as e:
        validate_data(data_df, {0, 1, 2, 3})

    assert str(e.value) == "No tokens column found in data.json"


def test_validate_data_not_lists() -> None:
    data_df = pd.DataFrame({"tokens": [0, 1, 2, 3]})

    with pytest.raises(ValueError) as e:
        validate_data(data_df, {0, 1, 2, 3})

    assert str(e.value) == "Values in tokens column are not lists"


def test_validate_data_token_not_in_tokens_map() -> None:
    data_df = pd.DataFrame({"tokens": [[0, 1], [2, 3]]})

    with pytest.raises(ValueError) as e:
        validate_data(data_df, {0, 1, 2})

    assert str(e.value) == "Token 3 not found in tokens_map.json"


def test_validate_data() -> None:
    data_df = pd.DataFrame({"tokens": [[0, 1], [2, 3]]})

    validate_data(data_df, {0, 1, 2, 3})


# validate_tokens_map
def test_validate_tokens_map_no_token_column() -> None:
    tokens_map_df = pd.DataFrame({"not_token": ["hello", "world", "hey", "welcome"]})

    with pytest.raises(ValueError) as e:
        validate_tokens_map(tokens_map_df)

    assert str(e.value) == "No token column found in tokens_map.json"


def test_validate_tokens_map_not_unique() -> None:
    tokens_map_df = pd.DataFrame({"token": ["hello", "world", "hey", "hey"]})

    with pytest.raises(ValueError) as e:
        validate_tokens_map(tokens_map_df)

    assert str(e.value) == "Duplicate tokens found in tokens_map.json"


def test_validate_tokens_map_index_not_unique() -> None:
    tokens_map_df = pd.DataFrame({"token": ["hello", "world", "hey", "welcome"]})
    tokens_map_df.index = [0, 1, 1, 3]

    with pytest.raises(ValueError) as e:
        validate_tokens_map(tokens_map_df)

    assert str(e.value) == "Duplicate tokens ids found in tokens_map.json"


def test_validate_tokens_map() -> None:
    tokens_map_df = pd.DataFrame({"token": ["hello", "world", "hey", "welcome"]})

    validate_tokens_map(tokens_map_df)


# get_dif_sets_map
def test_get_dif_sets_map() -> None:
    data: dict[int, list[int]] = {
        0: [0, 1, 2],
        1: [0, 1, 2],
        2: [0, 1, 2],
        3: [0, 1],
        4: [1, 2, 3],
    }
    all_tokens_ids: set[int] = {0, 1, 2, 3}

    dif_sets_map: dict[int, set[int]] = get_dif_sets_map(data, all_tokens_ids)

    assert dif_sets_map == {0: {4}, 1: set(), 2: {3}, 3: {0, 1, 2, 3}}


# DeclatNode
def test_DeclatNode() -> None:
    tokens_ids: list[int] = [0, 1]
    support: int = 4
    dif_set: set[int] = set()
    node: DeclatNode = DeclatNode(tokens_ids, support, dif_set)

    tokens_ids = [0, 1, 2]
    support = 3
    dif_set = {3}
    child: DeclatNode = DeclatNode(tokens_ids, support, dif_set)

    node.add_child(child)

    assert node.tokens_ids == [0, 1]
    assert node.support == 4
    assert node.dif_set == set()
    assert node.children == [child]
    assert node.tokens == []

    tokens_map: dict[int, str] = {
        0: "hello",
        1: "world",
        2: "hey",
        3: "welcome",
    }
    node.decode(tokens_map)

    assert node.tokens == ["hello", "world"]
    assert node.children[0].tokens == ["hello", "world", "hey"]


# build_declat_root
def test_build_declat_root() -> None:
    empty_set: set[int] = set()
    dif_sets_map: dict[int, set[int]] = {0: {4}, 1: empty_set, 2: {3}, 3: {0, 1, 2, 3}}
    num_transactions: int = 5
    min_support: int = 2

    root: DeclatNode = build_declat_root(dif_sets_map, num_transactions, min_support)

    assert root.tokens_ids == []
    assert root.support == 5
    assert root.dif_set == set()
    assert root.children == [
        DeclatNode([0], 4, {4}),
        DeclatNode([1], 5, set()),
        DeclatNode([2], 4, {3}),
    ]


# build_declat_tree
def test_build_declat_tree() -> None:
    empty_set: set[int] = set()
    dif_sets_map: dict[int, set[int]] = {0: {4}, 1: empty_set, 2: {3}, 3: {0, 1, 2, 3}}
    num_transactions: int = 5
    min_support: int = 2

    root: DeclatNode = build_declat_root(dif_sets_map, num_transactions, min_support)

    build_declat_tree(root.children, min_support)

    assert root.tokens_ids == []
    assert root.support == 5
    assert root.dif_set == set()
    assert root.children == [
        DeclatNode([0], 4, {4}),
        DeclatNode([1], 5, set()),
        DeclatNode([2], 4, {3}),
    ]

    assert root.children[0].tokens_ids == [0]
    assert root.children[0].support == 4
    assert root.children[0].dif_set == {4}
    assert root.children[0].children == [
        DeclatNode([0, 1], 4, set()),
        DeclatNode([0, 2], 3, {3}),
    ]

    assert root.children[1].tokens_ids == [1]
    assert root.children[1].support == 5
    assert root.children[1].dif_set == set()
    assert root.children[1].children == [
        DeclatNode([1, 2], 4, {3}),
    ]

    assert root.children[2].tokens_ids == [2]
    assert root.children[2].support == 4
    assert root.children[2].dif_set == {3}
    assert root.children[2].children == []

    assert root.children[0].children[0].tokens_ids == [0, 1]
    assert root.children[0].children[0].support == 4
    assert root.children[0].children[0].dif_set == set()
    assert root.children[0].children[0].children == [
        DeclatNode([0, 1, 2], 3, {3}),
    ]

    assert root.children[0].children[1].tokens_ids == [0, 2]
    assert root.children[0].children[1].support == 3
    assert root.children[0].children[1].dif_set == {3}
    assert root.children[0].children[1].children == []

    assert root.children[1].children[0].tokens_ids == [1, 2]
    assert root.children[1].children[0].support == 4
    assert root.children[1].children[0].dif_set == {3}
    assert root.children[1].children[0].children == []
