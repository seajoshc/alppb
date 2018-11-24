import sys
from unittest.mock import patch
import pytest
from alppb.alppb import main


def test_creating_python36_package_with_valid_input():
    testargs = ["alppb", "mlbgame", "rebukethe.net"]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_creating_python36_package_with_bad_bucket():
    pass
    testargs = ["alppb", "mlbgame", "rebukethenet"]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(Exception):
            main()
