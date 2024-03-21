import pytest


def pytest_collection_modifyitems(config, items):
    for item in items:
        # Check the file path of the current item (test function)
        file_path = str(item.fspath)

        if "/unit/" in file_path:
            # Dynamically add the "unit" marker
            item.add_marker(pytest.mark.unit)
        elif "/e2e/" in file_path:
            # Dynamically add the "e2e" marker
            item.add_marker(pytest.mark.e2e)
