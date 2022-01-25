import random
import re
import string


def replace_nth(candidate, sub, wanted, n):
    where = [m.start() for m in re.finditer(re.escape(sub), candidate)][n - 1]
    before = candidate[:where]
    after = candidate[where:]
    after = after.replace(sub, wanted, 1)
    result = before + after
    return result


def replace_random(candidate, sub, wanted):
    occurrences = [m.start() for m in re.finditer(re.escape(sub), candidate)]
    if not occurrences:
        return candidate

    pos = random.choice(occurrences)

    before = candidate[:pos]
    after = candidate[pos:]
    after = after.replace(sub, wanted, 1)

    result = before + after
    return result


def filter_candidates(symbols, payload):
    return [s for s in symbols.keys() if s in payload]


def random_char(spaces=True):
    chars = list(string.printable)
    chars_no_space = [c for c in chars if c not in string.whitespace]
    return random.choice(chars if spaces else chars_no_space)


def random_string(max_len=5, spaces=True):
    return "".join(
        [random_char(spaces=spaces) for i in range(random.randint(1, max_len))]
    )


def string_tautology():
    value_s = random_string(random.randint(1, 5))

    tautologies = [
        # Strings - equals
        "'{}'='{}'".format(value_s, value_s),
        "'{}' LIKE '{}'".format(value_s, value_s),
        '"{}"="{}"'.format(value_s, value_s),
        '"{}" LIKE "{}"'.format(value_s, value_s),
        # Strings - not equal
        "'{}'!='{}'".format(value_s, value_s + random_string(1, spaces=False)),
        "'{}'<>'{}'".format(value_s, value_s + random_string(1, spaces=False)),
        "'{}' NOT LIKE '{}'".format(value_s, value_s + random_string(1, spaces=False)),
        '"{}"!="{}"'.format(value_s, value_s + random_string(1, spaces=False)),
        '"{}"<>"{}"'.format(value_s, value_s + random_string(1, spaces=False)),
        '"{}" NOT LIKE "{}"'.format(value_s, value_s + random_string(1, spaces=False)),
    ]

    return random.choice(tautologies)


def string_contradiction():
    value_s = random_string(random.randint(1, 5))

    contradictions = [
        # Strings - equals
        "'{}'='{}'".format(value_s, value_s + random_string(1, spaces=False)),
        "'{}' LIKE '{}'".format(value_s, value_s + random_string(1, spaces=False)),
        '"{}"="{}"'.format(value_s, value_s + random_string(1, spaces=False)),
        '"{}" LIKE "{}"'.format(value_s, value_s + random_string(1, spaces=False)),
        # Strings - not equal
        "'{}'!='{}'".format(value_s, value_s),
        "'{}'<>'{}'".format(value_s, value_s),
        "'{}' NOT LIKE '{}'".format(value_s, value_s),
        '"{}"!="{}"'.format(value_s, value_s),
        '"{}"<>"{}"'.format(value_s, value_s),
        '"{}" NOT LIKE "{}"'.format(value_s, value_s),
    ]

    return random.choice(contradictions)


def num_tautology():
    value_n = random.randint(1, 10000)

    tautologies = [
        # Numbers - equal
        "{}={}".format(value_n, value_n),
        "{} LIKE {}".format(value_n, value_n),
        # Numbers - not equal
        "{}!={}".format(value_n, value_n + 1),
        "{}<>{}".format(value_n, value_n + 1),
        "{} NOT LIKE {}".format(value_n, value_n + 1),
        "{} IN ({},{},{})".format(value_n, value_n - 1, value_n, value_n + 1),
    ]

    return random.choice(tautologies)


def num_contradiction():
    value_n = random.randint(1, 10000)

    contradictions = [
        # Numbers - equal
        "{}={}".format(value_n, value_n + 1),
        "{} LIKE {}".format(value_n, value_n + 1),
        # Numbers - not equal
        "{}!={}".format(value_n, value_n),
        "{}<>{}".format(value_n, value_n),
        "{} NOT LIKE {}".format(value_n, value_n),
        "{} NOT IN ({},{},{})".format(value_n, value_n - 1, value_n, value_n + 1),
    ]

    return random.choice(contradictions)
