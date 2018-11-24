from alppb.codebuild import determine_image

def test_determine_image_python36():
    determined_imaged = determine_image("3.6")
    expected_image = "irlrobot/alppb-python36"
    print("DI: {}\nEI: {}".format(determined_imaged, expected_image))
    assert determined_imaged is expected_image
