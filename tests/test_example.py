"""
example_app.py のテストコード
"""

import sys
from pathlib import Path

# src ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from example_app import add


def test_add_positive_numbers():
    """正の数の加算テスト"""
    assert add(2, 3) == 5


def test_add_negative_numbers():
    """負の数の加算テスト"""
    assert add(-1, -1) == -2


def test_add_zero():
    """ゼロの加算テスト"""
    assert add(0, 5) == 5


if __name__ == "__main__":
    test_add_positive_numbers()
    test_add_negative_numbers()
    test_add_zero()
    print("All tests passed!")
