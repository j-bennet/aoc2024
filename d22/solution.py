from collections import Counter, deque
from functools import lru_cache
from os import path

ROOT_DIR = path.dirname(__file__)


def get_data(filename="input.txt"):
    full_name = path.join(ROOT_DIR, filename)
    with open(full_name) as f:
        return f.read().splitlines()


def parse_data(data):
    return [int(x) for x in data]


@lru_cache(maxsize=None)
def mix_prune(secret: int, val: int) -> int:
    """
    To mix a value into the secret number, calculate the bitwise XOR of the given value and
    the secret number. Then, the secret number becomes the result of that operation.
    To prune the secret number, calculate the value of the secret number modulo 16777216.
    Then, the secret number becomes the result of that operation.
    """
    return (secret ^ val) % 16777216


@lru_cache(maxsize=None)
def calculate_secret(secret):
    """
    In particular, each buyer's secret number evolves into the next secret number in the sequence via the
    following process:

    Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret
    number. Finally, prune the secret number.

    Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer.
    Then, mix this result into the secret number. Finally, prune the secret number.

    Calculate the result of multiplying the secret number by 2048. Then, mix this result into the
    secret number. Finally, prune the secret number.
    """
    val = secret << 6
    secret = mix_prune(secret, val)
    val = secret >> 5
    secret = mix_prune(secret, val)
    val = secret << 11
    secret = mix_prune(secret, val)
    return secret


def calculate_secret_n(secret, n):
    """
    Calculate the secret number after n iterations
    """
    for _ in range(n):
        secret = calculate_secret(secret)
    return secret


def score_sequences(number):
    """
    Credit to Alexandra Jay
    https://www.reddit.com/r/adventofcode/comments/1hjroap/comment/m3b1t0k/
    https://pastebin.com/Ad4WMj1j
    For part 2, I stored the 4 most recent deltas in a circular buffer,
    updating a Counter with the current price if this was the first time
    the sequence was encountered. After repeating this for each starting
    number, the answer was simply the largest count in the sum of all
    these counters.
    """
    current_sequence = deque([], maxlen=4)
    scores = Counter()

    for n in range(2000):
        if n >= 4:
            sequence = tuple(current_sequence)
            if sequence not in scores:  # only count the first appearance
                scores[tuple(current_sequence)] = number % 10

        new_number = calculate_secret(number)
        current_sequence.append((new_number % 10) - (number % 10))
        number = new_number

    return scores


def part1(data):
    """Part 1"""
    initials = parse_data(data)
    total = 0
    for x in initials:
        result = calculate_secret_n(x, 2000)
        # print(f"{x}: {result}")
        total += result
    return total


def part2(data):
    """Part 2"""
    initials = parse_data(data)
    total_scores = Counter()
    for x in initials:
        total_scores += score_sequences(x)
        # best_seq, result = total_scores.most_common(1)[0]
        # print(f"current best: {best_seq}, {result}")
    result = total_scores.most_common(1)[0][1]
    return result

if __name__ == "__main__":
    # print(f"Part 1: {part1(get_data('input.txt'))}")
    print(f"Part 2: {part2(get_data('input.txt'))}")
