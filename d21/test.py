from pprint import pprint

from solution import directional_to_directional_options, numeric_to_directional_options

assert numeric_to_directional_options("A", "0") == ["<A"]

assert numeric_to_directional_options("A", "02") == ["<A^A"]

assert set(numeric_to_directional_options("A", "029")) == {
    "<A^A^^>A",
    "<A^A^>^A",
    "<A^A>^^A",
}

assert set(numeric_to_directional_options("A", "029A")) == {
    "<A^A>^^AvvvA",
    "<A^A^>^AvvvA",
    "<A^A^^>AvvvA",
}

res = set()
for option in ["<A^A>^^AvvvA", "<A^A^>^AvvvA", "<A^A^^>AvvvA"]:
    res |= set(directional_to_directional_options("A", option))

pprint(res)
assert "v<<A>>^A<A>AvA<^AA>A<vAAA>^A" in res