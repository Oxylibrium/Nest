'''
Miscallaneous utils separate from the rest of Nest's core.
'''

from typing import List

def dictwalk(dictionary: dict, tree: List[str], fill: bool = False):
    """Walk down a dictionary tree and return an element.
    Parameters
    ----------
    dictionary: dict
        Dictionary to walk through.
    tree: list
        Sorted tree to walk down.
    fill: bool
        If true, create empty dictionaries
    """

    # Walk the pointer down the tree.
    # Python dictionaries are passed by reference,
    # So iterate over each element in the tree to arrive at
    # the last element.

    item = dictionary
    for k in tree:
        if k not in item:
            if fill:
                item[k] = {}
            else:
                raise ValueError(f'{k} not a valid key.')
        item = item[k]
    return item


def cog(category: str):
    '''
    Returns a metaclass to derive a cog from,
    with an __init__ function that declares the category.

    Arguments
    ---------
    category: str
        Category of the cog.
    '''

    # This cog has no functions beyond __init__ on purpose too
    # pylint: disable=R0903
    class Cog:
        '''
        Base class to derive a cog from.
        '''
        def __init__(self):
            self.category = category

    return Cog