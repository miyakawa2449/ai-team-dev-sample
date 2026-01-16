"""
シンプルな計算機能のサンプル実装
"""

def add(a: float, b: float) -> float:
    """
    2つの数値を加算する
    
    Args:
        a: 1つ目の数値
        b: 2つ目の数値
    
    Returns:
        加算結果
    """
    return a + b


if __name__ == "__main__":
    result = add(2, 3)
    print(f"2 + 3 = {result}")
