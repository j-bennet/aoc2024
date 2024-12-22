from pprint import pprint

from solution import numeric_to_directional_options

res = numeric_to_directional_options("A", "0")
pprint(res)

res = numeric_to_directional_options("A", "02")
pprint(res)

res = numeric_to_directional_options("A", "029")
pprint(res)

res = numeric_to_directional_options("A", "029A")
pprint(res)
