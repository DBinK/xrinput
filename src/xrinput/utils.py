
def round_list(_list: list[float], precision: int = 3) -> list[float]:
    """ 列表元素四舍五入 """
    return [round(x, precision) for x in _list]

def scale_list(_list: list[float], scale: float = 1.0) -> list[float]:
    """ 列表元素缩放 """
    return [x * scale for x in _list]

if __name__ == "__main__":
    print(round_list([1.001, 2.005, 3.008], 2))
    print(scale_list([1.0, 2.0, 3.0], 2.0))