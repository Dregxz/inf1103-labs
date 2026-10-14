"""Plain-function test runner (no classes, per the 100% procedural constraint).

    python tests/run_tests.py                    run every tests/test_*.py file
    python tests/run_tests.py test_ai_response   run only files whose name contains the text

No network, API key, Streamlit or Whisper install needed: those are replaced with fakes.
Shared fakes live in tests/helpers.py.
"""

import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)                        # tests/helpers.py
sys.path.insert(0, os.path.join(HERE, ".."))    # the managers

import io_manager


def test_files():
    """Names (without .py) of every test_*.py file next to this runner."""
    return sorted(f[:-3] for f in os.listdir(HERE) if f.startswith("test_") and f.endswith(".py"))


def discover(filters):
    """All (label, function) pairs from the test_*.py files that match the optional filters."""
    tests = []
    for name in test_files():
        if filters and not any(text in name for text in filters):
            continue
        module = importlib.import_module(name)
        for attribute in sorted(dir(module)):
            function = getattr(module, attribute)
            if attribute.startswith("test_") and callable(function) and function.__module__ == name:
                tests.append(("%s::%s" % (name, attribute), function))
    return tests


def explain_no_tests(filters):
    """A suite that runs nothing must not look like a pass: say what was searched and why it may be empty."""
    available = test_files()
    io_manager.show_error("no tests were found, so nothing was checked.")
    io_manager.show_message("  Looked for test_*.py files in: " + HERE)
    io_manager.show_message("  Test files found there: " + (", ".join(available) if available else "none"))
    if filters and available:
        io_manager.show_message("  Your filter %s matched none of them. Use part of a file name, e.g. test_ai_response."
                                % list(filters))
    elif not available:
        io_manager.show_message("  The tests live in separate files (one per area) next to run_tests.py. "
                                "If you copied only run_tests.py, also copy helpers.py and the test_*.py files "
                                "(or, in the team repo, wait until they are committed).")


def run_all(filters=()):
    tests = discover(filters)
    if not tests:
        explain_no_tests(filters)
        return 1
    failures = 0
    for label, function in tests:
        try:
            function()
            io_manager.show_message("PASS  " + label)
        except AssertionError as error:
            failures += 1
            io_manager.show_message("FAIL  %s %s" % (label, error))
        except Exception as error:  # noqa: BLE001 - report any crash as a failure
            failures += 1
            io_manager.show_message("ERROR %s: %r" % (label, error))
    files = len({label.split("::")[0] for label, _ in tests})
    io_manager.show_message("\n%d tests in %d files, %d failed" % (len(tests), files, failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run_all(sys.argv[1:]))
