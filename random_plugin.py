import pytest

# command line options
def pytest_addoption(parser):
    group = parser.getgroup("random", "randomize the tests to be run")
    group._addoption('--random',
        action="store_true",
        dest="random",
        default=False,
        help="randomize the tests to be run. defaults to False.")


def pytest_collection_modifyitems(session, config, items):
    """ called after collection has been performed, may filter or re-order
    the items in-place."""
    if not config.option.random:
        return

    item_set = set(items)
    new_order = []
    while len(item_set):
        new_order.append(item_set.pop())

    items[:] = new_order
