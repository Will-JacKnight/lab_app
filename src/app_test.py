from app import process_query


def test_knows_about_dinosaurs():
    assert process_query("dinosaurs") == ("Dinosaurs ruled "
                                          "the Earth 200 million years ago")


def test_does_not_know_about_asteroids():
    assert process_query("asteroids") == "Unknown"


def test_what_is_your_name():
    assert process_query("What is your name?") == "F4"


def test_largest_number():
    assert process_query("Which of the following \
numbers is the largest: 96, 93, 37?") == "96"


def test_plus():
    assert process_query("What is 51 plus 27?") == "78"


def test_minus():
    assert process_query("What is 51 minus 27?") == "24"
