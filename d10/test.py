from pprint import pprint

from solution import Map


def parse_str(data: str) -> Map:
    data = data.strip().splitlines()
    data = [line.strip() for line in data]
    return Map(data)


def test1():
    s = """
    0123
    1234
    8765
    9876
    """
    m = parse_str(s)
    # print(m.heights)
    pprint(dict(m.trails))


def test2():
    s = """
    89010123
    78121874
    87430965
    96549874
    45678903
    32019012
    01329801
    10456732
    """
    m = parse_str(s)
    pprint(dict(m.trails))
    print(m.score)


if __name__ == "__main__":
    test1()
    test2()
