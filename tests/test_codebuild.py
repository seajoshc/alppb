from alppb.codebuild import determine_image
from alppb.codebuild import pip_to_use


"""
alppb.codebuild.determine_image()
"""
def test_determine_image_python27():
    assert determine_image("2.7") == "irlrobot/alppb-python27"


def test_determine_image_python36():
    assert determine_image("3.6") == "irlrobot/alppb-python36"


def test_determine_image_python37():
    assert determine_image("3.7") == "irlrobot/alppb-python37"


def test_determine_image_default():
    """ Fallback to the python 3.6 image """
    assert determine_image("None") == "irlrobot/alppb-python36"


def test_determine_image_none():
    """ Fallback to the python 3.6 image """
    assert determine_image(None) == "irlrobot/alppb-python36"


def test_determine_image_invalid():
    """ Fallback to the python 3.6 image """
    assert determine_image("blah") == "irlrobot/alppb-python36"


"""
alppb.codebuild.pip_to_use()
"""
def test_pip_to_use_python27():
    assert pip_to_use("2.7") == "pip-2.7"


def test_pip_to_use_python36():
    assert pip_to_use("3.6") == "pip-3.6"


def test_pip_to_use_python37():
    assert pip_to_use("3.7") == "pip3.7"


def test_pip_to_use_default():
    """ Fallback to pip-3.6 """
    assert pip_to_use("None") == "pip-3.6"


def test_pip_to_use_none():
    """ Fallback to pip-3.6 """
    assert pip_to_use(None) == "pip-3.6"


def test_pip_to_use_invalid():
    """ Fallback to pip-3.6 """
    assert pip_to_use("blah") == "pip-3.6"
