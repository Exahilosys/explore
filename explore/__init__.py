import difflib
import functools
import math

from . import abstract


__all__ = ('single', 'specific', 'multiple', 'generic', 'lead', 'pick')


def single(value, argument):

    """
    Get the best matcher ratio of the two values.

    .. code-block:: py

        >>> single('alpha', 'theta')
        0.4
    """

    matcher = difflib.SequenceMatcher(a = argument, b = value)

    ratio = matcher.ratio()

    return ratio


key = type(
    '',
    (),
    {
        '__call__': lambda s, v: v.lower(),
        '__repr__': lambda s: 'str.lower'
    }
)()


def specific(values, argument, key = key):

    """
    Get (value, score) pairs for values against the argument.

    .. code-block:: py

        >>> values = ('aplha', 'beta', 'gamma')
        >>> pairs = specific(values, 'theta')
        >>> tuple(pairs) # generator
        (('aplha', 0.4), ('beta', 0.6), ('gamma', 0.2))
    """

    return abstract.specific(single, values, argument, key = key)


def multiple(values, argument, key = key):

    """
    Get the highest best score against the argument.

    .. code-block:: py

        >>> values = ('aplha', 'beta', 'gamma')
        >>> multiple(values, 'theta')
        0.6
    """

    assets = specific(values, argument, key = key)

    (junk, ratios) = zip(*assets)

    ratio = max(ratios)

    return ratio


def generic(fetch, values, argument, key = key):

    """
    Get (value, score) pairs for value's attributes against argument.

    .. code-block:: py

        >>> animals = [
        >>>     {'name': 'husky', 'type': 'dog', 'colors': ['white', 'grey']},
        >>>     {'name': 'ocelot', 'type': 'cat', 'colors': ['gold', 'black']},
        >>>     {'name': 'flamingo', 'type': 'bird', 'colors': ['pink']},
        >>>     # ...
        >>> ]
        >>> naty = lambda animal: (animal['name'], animal['type'])
        >>> pairs = generic(naty, animals, 'ligon')
        >>> tuple(pairs) # generator
        (
            ({'name': 'husky', ...}, 0.25),
            ({'name': 'ocelot', ...}, 0.36),
            ({'name': 'flamingo', ...}, 0.61)
        )
    """

    rank = functools.partial(multiple, key = key)

    return abstract.generic(rank, fetch, values, argument)


def differentiate(pair, stop = math.inf):

    """
    Overglorified sorting key.
    """

    (value, score) = pair

    if not score < stop:
        raise ValueError(pair)

    return score


def rank(pairs, reverse = False, safe = False):

    """
    Use on results similar from the exposed functions.
    """

    stop = 1 if safe else math.inf

    key = functools.partial(differentiate, stop = stop)

    return sorted(pairs, key = key, reverse = not reverse)


def lead(pairs, quick = True):

    """
    Get the highest scored pair.

    .. code-block:: py

        >>> # ...
        >>> lead(pairs)
        ({'name': 'flamingo', ...}, 0.61)
    """

    try:
        (leader, *lowers) = rank(pairs, safe = quick)
    except ValueError as error:
        (leader,) = error.args

    return leader


def pick(values, argument, fetch = None, key = key, score = False):

    """
    Get the best value matching the argument. If ``fetch`` is used, attribute
    search commences.

    .. code-block:: py

        >>> # ...
        >>> pick(animals, 'ligon', fetch = naty)
        {'name': 'flamingo', ...}
        >>> pick(animals, 'letc', fetch = naty, score = True)
        ({'name', 'ocelot', ...}, 0.4)# include score
    """

    if key:
        argument = key(argument)

    args = (generic, fetch) if fetch else (specific,)

    pairs = functools.partial(*args)(values, argument, key = key)

    result = lead(pairs, quick = True)

    if not score:
        result = result[0]

    return result
