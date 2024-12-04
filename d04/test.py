from solution import Grid

if __name__ == "__main__":
    data = [
        list("MAS"),
        list("MAS"),
        list("MAS"),
    ]
    g = Grid(data)
    print(g.count_all_mas())

    data = [
        list("SAM"),
        list("SAM"),
        list("SAM"),
    ]
    g = Grid(data)
    print(g.count_all_mas())
