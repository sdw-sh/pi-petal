def find(list, condition):
    for element in list:
        if condition(element):
            return element
    return None
