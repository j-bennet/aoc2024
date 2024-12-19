from solution import fits

assert fits("hello", 0, "he") == True
assert fits("hello", 0, "el") == False
assert fits("hello", 1, "el") == True
assert fits("hello", 1, "lo") == False
