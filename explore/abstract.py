

__all__ = ()


def _specific(key, rank, argument, value):

    check = key(value) if key else value

    score = rank(check, argument)

    return score


def specific(rank, values, argument, key = None):

    """
    Yield (value, score) pairs from values against the argument, according to
    rank, after transformation by key if used.
    """

    for value in values:
        score = _specific(key, rank, argument, value)
        yield (value, score)


def _generic(rank, fetch, argument, value):

    generate = fetch(value)

    attributes = tuple(generate)

    score = rank(attributes, argument) if attributes else 0

    return score


def generic(rank, fetch, values, argument):

    """
    Yield (value, score) pairs from values' attributes against the argument,
    according to rank.
    """

    for value in values:
        score = _generic(rank, fetch, argument, value)
        yield (value, score)
