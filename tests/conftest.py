import pytest
import datetime
import os
import sys

from fixtures.mock_alias_api import mock_alias_api_module

# ###############################################################################
# # pytest configuration
# ###############################################################################

# Ideally python 2 tests could be ignore using this 'collect_ignore' but it does
# not seem to work
# collect_ignore = ["tests/test_menu_generation.py", "tests/tke_scene_data_validator.py"]


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """

    # Ensure the Alias version is set for testing. Default to 2022.2.
    if not os.environ.get("TK_ALIAS_VERSION"):
        os.environ["TK_ALIAS_VERSION"] = "2022.2"
    print("Testing with Alias v{}".format(os.environ.get("TK_ALIAS_VERSION")))

    # Get the Alias bin directory and prepend it to the front of the env path var
    # NOTE This requires the build machines to have Alias installed at this location
    #
    alias_bin_path = os.environ.get(
        "TK_ALIAS_INSTALL_PATH",
        "C:\\Program Files\\Autodesk\\AliasSurface{version}\\bin".format(
            version=os.environ["TK_ALIAS_VERSION"]
        ),
    )
    print("Prepending to PATH: {}".format(alias_bin_path))
    os.environ["PATH"] = "{alias_bin_path};{path}".format(
        alias_bin_path=alias_bin_path,
        path=os.environ.get("PATH"),
    )

    # Add the tk_alias modules to the sys.path so unit tests can import the modules to test
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "python"))
    engine_dir = os.path.abspath(os.path.join(base_dir, "tk_alias"))
    api_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "api",
        )
    )
    paths = [
        api_dir,
        base_dir,
        engine_dir,
    ]
    print("Adding tk-alias folders:\n{}".format("\n".join(paths)))
    sys.path.extend(paths)

    try:
        import alias_api

        # Successfully imported the Alias Python API, display its info
        print(
            "Alias Python API v{} (compiled with Alias v{})".format(
                alias_api.__version__, alias_api.__alias_version__
            )
        )

        # Initialize the universe for testing
        alias_api.initialize_universe()

    except Exception as e:
        # No access to the alias_api module, let's mock it.
        print("Failed to import the Alias Python API\n{}".format(e))
        print("Mocking the Alias Python API")
        sys.modules["alias_api"] = mock_alias_api_module()


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """

    print("Timestamp:  {}".format(datetime.datetime.now()))


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """


# ###############################################################################
# Global Fixtures
# ###############################################################################


@pytest.fixture(autouse=True)
def skip_if_open_model(request):
    """
    Fixture to skip test cases if Alias mode is OpenModel and not being mocked.
    """

    if request.node.get_closest_marker("skip_open_model"):
        import alias_api

        is_mock = hasattr(alias_api, "__mode__") and alias_api.__mode__ == "mock"
        if not is_mock and os.path.basename(sys.executable) != "Alias.exe":
            pytest.skip("skipped for Alias OpenModel")
