import random
import re

from .fuzz_utils import (
    replace_random,
    filter_candidates,
    random_string,
    num_tautology,
    string_tautology,
    num_contradiction,
    string_contradiction,
)


def reset_inline_comments(payload: str):
    positions = list(re.finditer(r"/\*[^(/\*|\*/)]*\*/", payload))

    if not positions:
        return payload

    pos = random.choice(positions).span()

    replacements = ["/**/"]

    replacement = random.choice(replacements)

    new_payload = payload[: pos[0]] + replacement + payload[pos[1]:]

    return new_payload


def logical_invariant(payload):
    pos = re.search("(#|-- )", payload)

    if not pos:
        # No comments found
        return payload

    pos = pos.start()

    replacement = random.choice(
        [
            # AND True
            " AND 1",
            " AND True",
            " AND " + num_tautology(),
            " AND " + string_tautology(),
            # OR False
            " OR 0",
            " OR False",
            " OR " + num_contradiction(),
            " OR " + string_contradiction(),
        ]
    )

    new_payload = payload[:pos] + replacement + payload[pos:]

    return new_payload


def change_tautologies(payload):
    results = list(re.finditer(r'((?<=[^\'"\d\wx])\d+(?=[^\'"\d\wx]))=\1', payload))
    if not results:
        return payload
    candidate = random.choice(results)

    replacements = [num_tautology(), string_tautology()]

    replacement = random.choice(replacements)

    new_payload = (
            payload[: candidate.span()[0]] + replacement + payload[candidate.span()[1]:]
    )

    return new_payload


def spaces_to_comments(payload):
    symbols = {
        "[blank]": ["/**/", "%20", "+"],
        "/**/": ["[blank]", "%20", "+"],
        "%20": ["[blank]", "/**/", "+"],
        "+": ["[blank]", "/**/", "%20"],
    }

    symbols_in_payload = filter_candidates(symbols, payload)

    if not symbols_in_payload:
        return payload

    # Randomly choose symbol
    candidate_symbol = random.choice(symbols_in_payload)
    # Check for possible replacements
    replacements = symbols[candidate_symbol]
    # Choose one replacement randomly
    candidate_replacement = random.choice(replacements)

    # Apply mutation at one random occurrence in the payload
    return replace_random(payload, candidate_symbol, candidate_replacement)


def spaces_to_whitespaces_alternatives(payload):
    symbols = {
        "%20": ["%2f", "%09", "%0A", "%0C", "%0D"],
        "%2f": ["%20", "%09", "%0A", "%0C", "%0D"],
        "%09": ["%2f", "%20", "%0A", "%0C", "%0D"],
        "%0A": ["%2f", "%09", "%20", "%0C", "%0D"],
        "%0C": ["%2f", "%09", "%0A", "%20", "%0D"],
        "%0D": ["%2f", "%09", "%0A", "%0C", "%20"],
    }

    symbols_in_payload = filter_candidates(symbols, payload)

    if not symbols_in_payload:
        return payload

    # Randomly choose symbol
    candidate_symbol = random.choice(symbols_in_payload)
    # Check for possible replacements
    replacements = symbols[candidate_symbol]
    # Choose one replacement randomly
    candidate_replacement = random.choice(replacements)

    # Apply mutation at one random occurrence in the payload
    return replace_random(payload, candidate_symbol, candidate_replacement)


def random_case(payload):
    new_payload = []

    for c in payload:
        if random.random() > 0.5:
            c = c.swapcase()
        new_payload.append(c)

    return "".join(new_payload)


def comment_rewriting(payload):
    p = random.random()

    if p < 0.5 and ("#" in payload or "-- " in payload):
        return payload + random_string(2)
    elif p >= 0.5 and ("*/" in payload):
        return replace_random(payload, "*/", random_string() + "*/")
    else:
        return payload


def swap_int_repr(payload):
    candidates = list(re.finditer(r'(?<=[^\'"\d\wx])\d+(?=[^\'"\d\wx])', payload))

    if not candidates:
        return payload

    candidate_pos = random.choice(candidates).span()

    candidate = payload[candidate_pos[0]: candidate_pos[1]]

    replacements = [
        hex(int(candidate)),
        "(SELECT {})".format(candidate),
        # "({})".format(candidate),
    ]

    replacement = random.choice(replacements)

    return payload[: candidate_pos[0]] + replacement + payload[candidate_pos[1]:]


def swap_keywords(payload):
    symbols = {
        # OR
        "||": ["or"],
        "or": ["||"],
        # AND
        "&&": ["and"],
        "and": ["&&"],
        # Not equals
        "<>": ["!=", " NOT LIKE "],
        "!=": [" != ", "<>", " <> ", " NOT LIKE "],
        # Equals
        " = ": [" like "],
        " like ": [" = "],
    }

    symbols_in_payload = filter_candidates(symbols, payload)

    if not symbols_in_payload:
        return payload

    # Randomly choose symbol
    candidate_symbol = random.choice(symbols_in_payload)
    # Check for possible replacements
    replacements = symbols[candidate_symbol]
    # Choose one replacement randomly
    candidate_replacement = random.choice(replacements)

    # Apply mutation at one random occurrence in the payload
    return replace_random(payload, candidate_symbol, candidate_replacement)


class Fuzzer(object):
    strategies = [
        spaces_to_comments,
        random_case,
        swap_keywords,
        # swap_int_repr,
        spaces_to_whitespaces_alternatives,
        comment_rewriting,
        change_tautologies,
        # logical_invariant,
        reset_inline_comments,
    ]

    def __init__(self, payload):
        self.initial_payload = payload
        self.payload = payload

    def fuzz(self):
        strategy = random.choice(self.strategies)

        self.payload = strategy(self.initial_payload)

        return self.payload

    def current(self):
        return self.payload

    def reset(self):
        self.payload = self.initial_payload
        return self.payload
