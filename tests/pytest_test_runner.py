class PytestTestRunner:
    """Runs pytest to discover and run tests."""

    @classmethod
    def add_arguments(cls, parser):
        parser.set_defaults(keepdb=True)

        # remaps to the -k cli arg of pytest, useful for test selection
        parser.add_argument(
            "-s",
            "--select",
            help="remaps to -k test-selection argument in pytest",
        )

        parser.add_argument(
            "--selenium",
            action="store_true",
            help="run selenium tests",
        )

    def __init__(
        self,
        verbosity=1,
        failfast=False,
        keepdb=True,
        select=None,
        selenium=False,
        **kwargs,
    ):
        self.verbosity = verbosity
        self.failfast = failfast
        self.keepdb = keepdb
        self.select = select
        self.selenium = selenium

    def run_tests(self, test_labels):
        """Run pytest and return the exitcode.

        It translates some of Django's test command option to pytest's.
        """
        import pytest

        argv = []
        if self.select is not None:
            argv.append(f"-k {self.select}")
        if self.verbosity == 0:
            argv.append("--quiet")
        if self.verbosity == 2:
            argv.append("--verbose")
        if self.verbosity == 3:
            argv.append("-vv")
        if self.failfast:
            argv.append("--exitfirst")
        if self.keepdb:
            argv.append("--reuse-db")
        if self.selenium:
            argv.append("-m selenium")

        argv.extend(test_labels)
        return pytest.main(argv)
