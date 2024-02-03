from typing import List, Any, Callable


def find(list: List[Any], condition: Callable):
    for element in list:
        if condition(element):
            return element
    return None


def index_exists(list: List[Any], index: int) -> bool:
    """
    checks if an index in a list exists
    only checks for 0 and positive indices
    as any decent function would
    """
    return index < len(list)
