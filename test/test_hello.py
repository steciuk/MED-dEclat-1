import pytest

from hello.hello import Hello


def test_sum() -> None:
    hello = Hello('abc')
    assert hello.sum(1, 2, 3) == 6


def test_raises() -> None:
    hello = Hello('abc')
    with pytest.raises(ValueError):
        hello.raises()
