
from solution import (
    dir_to_dir_options,
    find_shortest_option_length,
    minimum_sequence,
    num_to_dir_options,
)

assert num_to_dir_options("0") == ["<A"]

assert num_to_dir_options("02") == ["<A^A"]

assert set(num_to_dir_options("029")) == {
    "<A^A^^>A",
    "<A^A^>^A",
    "<A^A>^^A",
}

assert set(num_to_dir_options("029A")) == {
    "<A^A>^^AvvvA",
    "<A^A^>^AvvvA",
    "<A^A^^>AvvvA",
}

res = set()
for option in ["<A^A>^^AvvvA", "<A^A^>^AvvvA", "<A^A^^>AvvvA"]:
    res |= set(dir_to_dir_options(option))
assert "v<<A>>^A<A>AvA<^AA>A<vAAA>^A" in res

assert find_shortest_option_length("029A") == 68

assert minimum_sequence(0, "029A", 2) == 68