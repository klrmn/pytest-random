pytest-random
=============

randomize your py.test run

The randomization algorithm is not the least bit sophisticated, so do not depend on this plugin for a specific degree of randomness. Please use the --verbose option to see the randomization for yourself.

example usage:
    py.test . --random

options:
    --random            randomize the tests to be run. defaults to False.
    --random-group      group by fixtures to avoid multiple setUp/tearDown
                        calls. defaults to False.
    --random-seed=RANDOM_SEED
                        the seed to use for randomization if you need to
                        repeat a run.
