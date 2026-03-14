from .test import run as _test_run
from .create_problem import run as _create_run

COMMANDS = {
    "test": _test_run,
    "create:problem": _create_run,
}
