import pandas as pd
import pytest

from get_reddit import create_token_ids, remove_duplicates_in_rows, remove_non_alpha


def test_remove_non_alpha():
    series = pd.Series(["Hello, world!", " Hello,,,   wor234ld!"])
    result = remove_non_alpha(series)
    assert result[0] == "Hello world"
    assert result[1] == " Hello   world"

    series = pd.Series(dtype=str)
    result = remove_non_alpha(series)
    assert result.empty


def test_remove_duplicates_in_rows():
    series = pd.Series([["hello", "world", "hello"], ["hello", "world"]])
    result = remove_duplicates_in_rows(series)
    assert result[0] == ["hello", "world"]
    assert result[1] == ["hello", "world"]

    series = pd.Series(dtype=object)
    result = remove_duplicates_in_rows(series)
    assert result.empty


def test_create_token_ids():
    series = pd.Series(
        [["hello", "world"], [], ["hey", "hello", "world"], ["hey", "welcome"]],
    )
    result, tokens_map = create_token_ids(series)
    assert result[0] == [0, 1]
    assert result[1] == []
    assert result[2] == [2, 0, 1]
    assert result[3] == [2, 3]
    assert tokens_map == {"hello": 0, "world": 1, "hey": 2, "welcome": 3}

    series = pd.Series(dtype=object)
    result, tokens_map = create_token_ids(series)
    assert result.empty
    assert tokens_map == {}
