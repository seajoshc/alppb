from alppb.codebuild import determine_image


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
