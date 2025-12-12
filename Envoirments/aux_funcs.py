def coords_to_key(x: int, y: int):
    return str(x) + "-" + str(y)


def key_to_coords(key: str):
    raw_numbers = key.split("-")
    numeric_list = []
    for n in raw_numbers:
        numeric_list.append(int(n))
    return numeric_list
