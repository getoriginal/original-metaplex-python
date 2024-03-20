from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def project_root(pytestconfig):
    return Path(pytestconfig.rootdir)
