def get_distance(F: float, S: float, m: float) -> float:
    return (2 * F * S) / (9.81 * m) / 10


if __name__ == "__main__":
    print(get_distance(13, 1.5, 8 * 10 ** -3))