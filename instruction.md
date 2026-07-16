# Fix unrecognized-option traceback in pylint

Fix the bug described below so that the failing test(s) pass, without breaking any other tests.

You are working in a checkout of the `pylint-dev/pylint` repository. Do not modify the test files themselves; change the library code so the existing/expected tests succeed.

---

## Issue

Traceback printed for unrecognized option

### Bug description

A traceback is printed when an unrecognized option is passed to pylint.

### Command used

```shell
pylint -Q
```

### Pylint output

```shell
************* Module Command line
Command line:1:0: E0015: Unrecognized option found: Q (unrecognized-option)
Traceback (most recent call last):
  File ".../bin/pylint", line 33, in <module>
    sys.exit(load_entry_point('pylint', 'console_scripts', 'pylint')())
  ...
  File ".../pylint/config/config_initialization.py", line 85, in _config_initialization
    raise _UnrecognizedOptionError(options=unrecognized_options)
pylint.config.exceptions._UnrecognizedOptionError
```

### Expected behavior

The useful diagnostic line is fine:

`Command line:1:0: E0015: Unrecognized option found: Q (unrecognized-option)`

The traceback is not expected and is not user-friendly. Prefer exiting via the argument parser with a usage message, similar to other CLIs (e.g. mypy), instead of raising an internal exception that dumps a stack trace.
