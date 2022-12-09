import pandas as pd
import pytest

from build_tree import (
    TreeNode,
    build_declat_root,
    build_declat_tree,
    build_eclat_root,
    build_eclat_tree,
    get_dif_sets_map,
    get_tid_sets_map,
    load_data,
    validate_data,
    validate_tokens_map,
)


# load_data
def test_load_data_missing_files() -> None:
    with pytest.raises(FileNotFoundError) as e:
        load_data("test/test_build_tree_data/missing_data")

    assert str(e.value) == "No data.json file found in the directory"

    with pytest.raises(FileNotFoundError) as e:
        load_data("test/test_build_tree_data/missing_tokens_map")

    assert str(e.value) == "No tokens_map.json file found in the directory"


def test_load_data() -> None:
    data_df, tokens_map_df = load_data("test/test_build_tree_data/valid")

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


# get_id_sets_map
def test_get_id_sets_map() -> None:
    data: dict[int, list[int]] = {
        0: [0, 1, 2],
        1: [0, 1, 2],
        2: [0, 1, 2],
        3: [0, 1],
        4: [1, 2, 3],
    }
    all_tokens_ids: set[int] = {0, 1, 2, 3}

    id_sets_map: dict[int, set[int]] = get_dif_sets_map(data, all_tokens_ids)

    assert id_sets_map == {0: {4}, 1: set(), 2: {3}, 3: {0, 1, 2, 3}}


# TreeNode
def test_TreeNode() -> None:
    tokens_ids: list[int] = [0, 1]
    support: int = 4
    id_set: set[int] = set()
    node: TreeNode = TreeNode(tokens_ids, support, id_set)

    tokens_ids = [0, 1, 2]
    support = 3
    id_set = {3}
    child: TreeNode = TreeNode(tokens_ids, support, id_set)

    node.add_child(child)

    assert node.tokens_ids == [0, 1]
    assert node.support == 4
    assert node.id_set == set()
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
    id_sets_map: dict[int, set[int]] = {0: {4}, 1: empty_set, 2: {3}, 3: {0, 1, 2, 3}}
    num_transactions: int = 5
    min_support: int = 2

    root: TreeNode = build_declat_root(id_sets_map, num_transactions, min_support)

    assert root.tokens_ids == []
    assert root.support == 5
    assert root.id_set == set()
    assert root.children == [
        TreeNode([0], 4, {4}),
        TreeNode([1], 5, set()),
        TreeNode([2], 4, {3}),
    ]


# build_declat_tree
def test_build_declat_tree() -> None:
    empty_set: set[int] = set()
    id_sets_map: dict[int, set[int]] = {0: {4}, 1: empty_set, 2: {3}, 3: {0, 1, 2, 3}}
    num_transactions: int = 5
    min_support: int = 2

    root: TreeNode = build_declat_root(id_sets_map, num_transactions, min_support)

    build_declat_tree(root.children, min_support)

    assert root.tokens_ids == []
    assert root.support == 5
    assert root.id_set == set()
    assert root.children == [
        TreeNode([0], 4, {4}),
        TreeNode([1], 5, set()),
        TreeNode([2], 4, {3}),
    ]

    assert root.children[0].tokens_ids == [0]
    assert root.children[0].support == 4
    assert root.children[0].id_set == {4}
    assert root.children[0].children == [
        TreeNode([0, 1], 4, set()),
        TreeNode([0, 2], 3, {3}),
    ]

    assert root.children[1].tokens_ids == [1]
    assert root.children[1].support == 5
    assert root.children[1].id_set == set()
    assert root.children[1].children == [
        TreeNode([1, 2], 4, {3}),
    ]

    assert root.children[2].tokens_ids == [2]
    assert root.children[2].support == 4
    assert root.children[2].id_set == {3}
    assert root.children[2].children == []

    assert root.children[0].children[0].tokens_ids == [0, 1]
    assert root.children[0].children[0].support == 4
    assert root.children[0].children[0].id_set == set()
    assert root.children[0].children[0].children == [
        TreeNode([0, 1, 2], 3, {3}),
    ]

    assert root.children[0].children[1].tokens_ids == [0, 2]
    assert root.children[0].children[1].support == 3
    assert root.children[0].children[1].id_set == {3}
    assert root.children[0].children[1].children == []

    assert root.children[1].children[0].tokens_ids == [1, 2]
    assert root.children[1].children[0].support == 4
    assert root.children[1].children[0].id_set == {3}
    assert root.children[1].children[0].children == []


# get_tid_sets_map
def test_get_tid_sets_map() -> None:
    data: dict[int, list[int]] = {
        0: [0, 1, 2],
        1: [0, 1, 2],
        2: [0, 1, 2],
        3: [0, 1],
        4: [1, 2, 3],
    }
    all_tokens_ids: set[int] = {0, 1, 2, 3}

    tid_sets_map: dict[int, set[int]] = get_tid_sets_map(data, all_tokens_ids)

    assert tid_sets_map == {
        0: {0, 1, 2, 3},
        1: {0, 1, 2, 3, 4},
        2: {0, 1, 2, 4},
        3: {4},
    }


# build_eclat_root
def test_build_eclat_root() -> None:
    tid_sets_map: dict[int, set[int]] = {
        0: {0, 1, 2, 3},
        1: {0, 1, 2, 3, 4},
        2: {0, 1, 2, 4},
        3: {4},
    }
    num_transactions: int = 5
    all_tokens_ids: set[int] = {0, 1, 2, 3}
    min_support: int = 2

    root: TreeNode = build_eclat_root(
        tid_sets_map, num_transactions, min_support, all_tokens_ids
    )

    assert root.tokens_ids == []
    assert root.support == 5
    assert root.id_set == {0, 1, 2, 3}

    assert root.children == [
        TreeNode([0], 4, {0, 1, 2, 3}),
        TreeNode([1], 5, {0, 1, 2, 3, 4}),
        TreeNode([2], 4, {0, 1, 2, 4}),
    ]


# build_eclat_tree
def test_build_eclat_tree() -> None:
    tid_sets_map: dict[int, set[int]] = {
        0: {0, 1, 2, 3},
        1: {0, 1, 2, 3, 4},
        2: {0, 1, 2, 4},
        3: {4},
    }
    num_transactions: int = 5
    all_tokens_ids: set[int] = {0, 1, 2, 3}
    min_support: int = 2

    root: TreeNode = build_eclat_root(
        tid_sets_map, num_transactions, min_support, all_tokens_ids
    )

    build_eclat_tree(root.children, min_support)

    assert root.tokens_ids == []
    assert root.support == 5
    assert root.id_set == {0, 1, 2, 3}
    assert root.children == [
        TreeNode([0], 4, {0, 1, 2, 3}),
        TreeNode([1], 5, {0, 1, 2, 3, 4}),
        TreeNode([2], 4, {0, 1, 2, 4}),
    ]

    assert root.children[0].tokens_ids == [0]
    assert root.children[0].support == 4
    assert root.children[0].id_set == {0, 1, 2, 3}
    assert root.children[0].children == [
        TreeNode([0, 1], 4, {0, 1, 2, 3}),
        TreeNode([0, 2], 3, {0, 1, 2}),
    ]

    assert root.children[1].tokens_ids == [1]
    assert root.children[1].support == 5
    assert root.children[1].id_set == {0, 1, 2, 3, 4}
    assert root.children[1].children == [
        TreeNode([1, 2], 4, {0, 1, 2, 4}),
    ]

    assert root.children[2].tokens_ids == [2]
    assert root.children[2].support == 4
    assert root.children[2].id_set == {0, 1, 2, 4}
    assert root.children[2].children == []

    assert root.children[0].children[0].tokens_ids == [0, 1]
    assert root.children[0].children[0].support == 4
    assert root.children[0].children[0].id_set == {0, 1, 2, 3}
    assert root.children[0].children[0].children == [
        TreeNode([0, 1, 2], 3, {0, 1, 2}),
    ]

    assert root.children[0].children[1].tokens_ids == [0, 2]
    assert root.children[0].children[1].support == 3
    assert root.children[0].children[1].id_set == {0, 1, 2}
    assert root.children[0].children[1].children == []

    assert root.children[1].children[0].tokens_ids == [1, 2]
    assert root.children[1].children[0].support == 4
    assert root.children[1].children[0].id_set == {0, 1, 2, 4}
    assert root.children[1].children[0].children == []
