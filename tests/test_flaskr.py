import os
import tempfile

import pytest

from flaskr import flaskr

@pytest.fixture
def client():
    