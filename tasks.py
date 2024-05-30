from typing import Any

import invoke
from invoke.context import Context, Result
from invoke.tasks import task

DEFAULT_RUN_PARAMS = {"warn": False, "echo": True, "pty": True}
_ORIGIN_MAIN = "origin/main"


@task
def checktypes(ctx: Context, base_branch: str = _ORIGIN_MAIN) -> None:
    """Static and consistency type checking using mypy.

    Doesn't warn if missing annotation in typeshed.

    Args:
    ctx: arbitrarily-named context argument used for transmission of "global" data
    or values loaded from configuration files.
    base_branch: branch path.
    """
    run_on_changed_python(
        ctx, cmd="mypy --no-warn-incomplete-stub", base_branch=base_branch
    )


@task
def pip_sync(ctx: Context) -> None:
    """Sync all dependencies.

    Install all requirements in the user's home directory
    to avoid root access request and display ascii
    progess bar.

    Args:
    ctx: arbitrarily-named context argument used for transmission of "global" data
    or values loaded from configuration files.
    """
    run(
        ctx,
        (
            "python3 -m piptools sync "
            "requirements.txt"
            "--pip-args '--user --progress-bar on'"
        ),
    )


@task
def checkformat(ctx: Context, base_branch: str = _ORIGIN_MAIN) -> None:
    """Check the source format.

    Check and report incorrectly formatted imports, code and docstrings
    using isort, black and docformatter.

    Args:
    ctx: arbitrarily-named context argument used for transmission of "global" data
        or values loaded from configuration files.
    base_branch: branch path.
    """
    run_on_changed_python(
        ctx,
        cmd="isort --python-version auto --profile black --diff --check",
        base_branch=base_branch,
    )
    run_on_changed_python(
        ctx,
        cmd="black --color --target-version py39 --diff --check",
        base_branch=base_branch,
    )
    run_on_changed_python(
        ctx,
        cmd="docformatter --black --wrap-descriptions 0 --check",
        base_branch=base_branch,
    )


@task
def checkerrors(ctx: Context, base_branch: str = _ORIGIN_MAIN) -> None:
    """Look for errors in the project using pyflakes.

    Examine the syntax tree of each Python file looking for logical errors.

    Args:
    ctx: arbitrarily-named context argument used for transmission of "global" data
    or values loaded from configuration files.
    base_branch: branch path.
    """
    run_on_changed_python(ctx, cmd="pyflakes", base_branch=base_branch)


@task
def checkimports(ctx: Context) -> None:
    """Look for errors in the project structure using import-linter.

    Check the arquitecture by analysing the imports between all the modules
    comparing them against a set of predifined rules.

    Args:
    ctx: arbitrarily-named context argument used for transmission of "global" data
    or values loaded from configuration files.
    """
    run(ctx, "lint-imports")


@task
def formatsource(ctx: Context, base_branch: str = _ORIGIN_MAIN) -> None:
    """Format the source for all the project.

    Sort imports alphabetically separated into sections and by type.
    Remove unused imports and variables from Python code.
    Format code to look the same and format docstrings
    to follow some PEP 257 and PEP 8 conventions.

    Args:
    ctx: arbitrarily-named context argument used for transmission of "global" data
    or values loaded from configuration files.
    base_branch: branch path.
    """
    run_on_changed_python(
        ctx,
        cmd="isort --python-version auto --profile black",
        base_branch=base_branch,
    )
    run_on_changed_python(
        ctx,
        cmd="autoflake -i -r --remove-all-unused-imports --ignore-init-module-imports",
        base_branch=base_branch,
    )
    run_on_changed_python(
        ctx, cmd="black --color --target-version py39", base_branch=base_branch
    )
    run_on_changed_python(
        ctx,
        cmd="docformatter --black --in-place --recursive --wrap-descriptions 0",
        base_branch=base_branch,
    )


@task
def unittests(
    ctx: Context,
    cores: str = "2",
    coverage_report: bool = False,
    html_report: bool = False,
    derandomize: bool = False,
    timeout: int = 2,
    all: bool = False,
) -> None:
    """Run unit tests.

    Run pytest showing the slowest 30 test execution times.
    Tests are grouped by module for 'test functions' and by class
    for 'test methods' those groups are distribuited to available
    workers as whole units. Pytest will display local variables
    in tracebacks and will only run tests matching "unittest"
    expression. Result files will be created in junit-xml style
    format at a given path

    Args:
    ctx: arbitrarily-named context argument used for transmission of "global" data
    or values loaded from configuration files.
    cores: to send tests to multiple CPUs, pass a number, or with -n auto, pytest-xdist
    will use as many processes as your computer has CPU cores.
    coverage_report: if true creates junit-xml style report
    """
    random_order = "--random-order"
    if derandomize:
        random_order = ""
    html_test_results_report = ""
    if html_report:
        html_test_results_report = "--html=test-results.html --self-contained-html"
    coverage_options = ""
    if coverage_report:
        coverage_options = (
            "--junitxml=junit/test-results.xml --cov-report=xml "
            "--cov-report=html --cov=bold "
            "-k 'not test_get_pricing_info and not test_pricing_commons and not test_sale_calculator'"
        )

    path_tests = "tests/"

    cmd = (
        f"pytest {random_order} --timeout={timeout} --durations=30 -n {cores} --dist loadscope "
        f"-l -m unittest {html_test_results_report} {coverage_options} {path_tests}"
    )
    if not run(ctx, cmd):
        raise invoke.Exit("Please fix the unit tests")


def run_on_changed_python(
    ctx: Context, cmd: str, base_branch: str, **kwargs: Any
) -> Result:
    """Execute a command over the locally modified files.

    Exclude changes outside the current directory showing only
    names of changed paths and ignore deleted ones, filter
    .py files then apply cmd to the result in groups of
    maximum 20 arguments, xargs won't run if there is no input.

    Args:
    ctx: arbitrarily-named context argument used for transmission of "global" data
    or values loaded from configuration files.
    base_branch: branch path.nv
    cmd: the shell command to execute.
    **kwargs:  all default kwargs will default to the values instance's context attribute,
    specifically in its configuration's run subtree.
    """
    return run(
        ctx,
        f"""git diff --relative --name-only {base_branch} --diff-filter d """
        f"""| grep '.py$' | xargs -t -n 20 --no-run-if-empty {cmd}""",
        **kwargs,
    )


def run(ctx: Context, cmd: str, **kwargs: Any) -> Result:
    """Execute cmd, returns an instance of Result.

    Args:
    ctx: arbitrarily-named context argument used for transmission of "global" data
    or values loaded from configuration files
    cmd: the shell command to execute
    **kwargs: all default kwargs will default to the values instance's context attribute,
    specifically in its configuration's run subtree
    """
    result = ctx.run(cmd, **DEFAULT_RUN_PARAMS, **kwargs)
    if not result:
        raise invoke.Exit(
            "The shell command couldn't run, the proccess was interrupted or didn't finish succesfully"
        )
    else:
        return result


@task(
    pre=[formatsource, checkerrors, checkimports, checktypes, unittests],
    default=True,
)
def prepare(ctx: Context) -> None:
    """Prepare the project before a PR.

    Run the following tasks: formatsource, checkerrors, checkimports, checktypes,


    Args:
    ctx: arbitrarily-named context argument used for transmission of "global" data
    or values loaded from configuration files.
    """
    run(ctx, "git status")
