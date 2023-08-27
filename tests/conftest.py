import pytest
from unittest.mock import MagicMock

@pytest.fixture(scope='function')
def magick_cursor():
    return MagicMock()
