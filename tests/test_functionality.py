import py, pytest

pytest_plugins = "pytester"


class TestFunctionality(object):

    def _set_things_up(self, testdir):
        # needs multiple directories
        testdir.tmpdir.ensure("__init__.py")

        # needs multiple files in a directory
        testdir.makepyfile(
            test_one="""
            def test_a():
                pass

            """,
            test_two="""
            def test_z():
                pass

            """)

        # needs mutliple plain tests in a file
        testdir.makepyfile(
            test_three="""
            def test_c():
                pass

            def test_b():
                pass

            """,
            test_four="""
            def test_y():
                pass

            def test_w():
                pass

            """
            )

        # needs multiple test classes in a file
        testdir.makepyfile("""
            class TestGimmel(object):
                def test_q(self):
                    pass

                def test_o(self):
                    pass

                def test_n(self):
                    pass

            class TestAleph(object):
                def test_d(self):
                    pass

                def test_e(self):
                    pass

                def test_f(self):
                    pass
            """)

        # collect expected output
        self.expected_output = testdir.runpytest('-p no:random', '--verbose')


    def test_tests_are_not_random(self, testdir):
        # set up prereqs
        self._set_things_up(testdir)

        # do non-randomized run
        actual_output = testdir.runpytest('--verbose')

        # compare to standard
        assert actual_output.outlines[6:-1] == self.expected_output.outlines[6:-1]


    def test_tests_are_random(self, testdir):
        # set up prereqs
        self._set_things_up(testdir)

        # do randomized run & compare to standard
        actual_output = testdir.runpytest('--random', '--verbose')
        assert actual_output.outlines[6:-1] != self.expected_output.outlines[6:-1]

        # do 10 randomized runs & campare to other randomized runs
        run_results = [ actual_output.outlines[6:-1], self.expected_output.outlines[6:-1] ]
        for x in range(10):
            actual_output = testdir.runpytest('--random', '--verbose')
            assert not actual_output.outlines[6:-1] in run_results
            run_results.append(actual_output.outlines[6:-1])


    def test_seed_is_written_and_can_be_set(self, testdir):
        # set up prereqs
        self._set_things_up(testdir)

        # do randomized run
        first_output = testdir.runpytest('--random', '--verbose')
        # get the seed
        seedline = [x for x in first_output.outlines if x.startswith(u'Tests are shuffled')]
        assert len(seedline) == 1
        seed = int(seedline[0].split()[-1].strip('.'))
        # second run should be the same order
        second_output = testdir.runpytest('--random', '--random-seed', str(seed), '--verbose')
        assert first_output.outlines[6:-1] == second_output.outlines[6:-1]
        # third run with different seed should be different
        third_output = testdir.runpytest('--random', '--random-seed', str(seed + 1), '--verbose')
        assert first_output.outlines[6:-1] != third_output.outlines[6:-1]
