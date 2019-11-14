import difflib
import functools

from . import abstract


__all__ = ('single', 'specific', 'multiple', 'generic', 'lead', 'pick')


def single(value, argument):

    """
    Return the best matcher ratio of the two values.

    .. code-block::

        >>> score = single('alpha', 'theta')
        >>> 0.4
    """

    matcher = difflib.SequenceMatcher(a = argument, b = value)

    ratio = matcher.ratio()

    return ratio


key = type('', (), {'__call__': str.lower, '__repr__': lambda s: 'str.lower'})()


def specific(values, argument, key = key):

    """
    Return (value, score) pairs for values against the argument.

    .. code-block::

        >>> values = ('aplha', 'beta', 'gamma')
        >>> pairs = specific(values, 'theta')
        >>> pairs = tuple(pairs) # generator
        >>> (('aplha', 0.4), ('beta', 0.6), ('gamma', 0.2))
    """

    return abstract.specific(single, values, argument, key = key)


def multiple(values, argument, key = key):

    """
    Return the highest best score against the argument.

    .. code-block::

        >>> values = ('aplha', 'beta', 'gamma')
        >>> score = multiple(values, 'theta')
        >>> 0.6
    """

    assets = specific(values, argument, key = key)

    (junk, ratios) = zip(*assets)

    ratio = max(ratios)

    return ratio


def generic(fetch, values, argument, key = key):

    """
    Return (value, score) pairs for value's attributes against argument.

    .. code-block::

        >>> animals = [
        >>>     {'name': 'husky', 'type': 'dog', 'colors': ['white', 'grey']},
        >>>     {'name': 'ocelot', 'type': 'cat', 'colors': ['gold', 'black']},
        >>>     {'name': 'flamingo', 'type': 'bird', 'colors': ['pink']},
        >>>     # ...
        >>> ]
        >>> naty = lambda animal: (animal['name'], animal['type'])
        >>> pairs = generic(naty, animals, 'ligon')
        >>> pairs = tuple(pairs) # generator
        >>> (
        >>>     ({'name': 'husky', ...}, 0.25),
        >>>     ({'name': 'ocelot', ...}, 0.36),
        >>>     ({'name': 'flamingo', ...}, 0.61)
        >>> )
    """

    rank = functools.partial(multiple, key = key)

    return abstract.generic(rank, fetch, values, argument)


def differentiate(pair):

    """
    Overglorified sorting key.
    """

    (value, score) = pair

    return score


def rank(pairs, reverse = False):

    """
    Use on results similar from the exposed functions.
    """

    return sorted(pairs, key = differentiate, reverse = not reverse)


def lead(pairs):

    """
    Return the highest scored pair.

    .. code-block::

        >>> # ...
        >>> best = lead(pairs)
        >>> ({'name': 'flamingo', ...}, 0.61)
    """

    (leader, *lowers) = rank(pairs)

    return leader


def pick(values, argument, fetch = None, key = key):

    """
    Return the best value matching the argument.
    If fetch is used, attribute-based search is commences.

    .. code-block::

        >>> # ...
        >>> best = pick(animals, 'ligon', fetch = naty)
        >>> {'name': 'flamingo', ...}
    """

    if key:

        argument = key(argument)

    args = (generic, fetch) if fetch else (specific,)

    pairs = functools.partial(*args)(values, argument, key = key)

    (score, value) = lead(pairs)

    return value
