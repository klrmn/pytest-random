import pytest, random

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

    items = random.shuffle(items)
