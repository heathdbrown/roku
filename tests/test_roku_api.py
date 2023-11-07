import pytest

from roku.api import to_snake_case
from roku.api import remap_keys

TEST_SNAKE_CASE = [
    #(input_string, expected)
    ("test", "test"),
    ("testTest", "test_test"),
    ("testTEST", "test_test"),
    ("test2Test", "test2_test"),
    ("TestTest", "test_test"),
    ("test-test", "test_test"),
    ("Test-test", "test_test"),
    ("TestTest-test", "test_test_test"),
    ("test-test-test", "test_test_test"),
    ("test-test-test-test", "test_test_test_test")
    # Fails("Testtest-test", "test_test_test")
]

TEST_UGLY_DICT = [
    #(test, expected)
    ({}, {}),
    ({"friendlyName": "test"}, {"friendly_name":"test"})
]

@pytest.mark.parametrize("input_string,expected", TEST_SNAKE_CASE)
def test_to_snake_case(input_string, expected):
    assert to_snake_case(input_string) == expected

@pytest.mark.parametrize("test, expected", TEST_UGLY_DICT)
def test_remap_keys(test, expected):
    assert remap_keys(test) == expected