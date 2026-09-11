from text_parser import (
    normalize_whitespace,
    parse_entry,
    parse_timesheet,
)


def test_normalize_whitespace():
    text = "10   Lynnwood\n6.00   -   3.30"

    result = normalize_whitespace(text)

    assert result == "10 Lynnwood 6.00 - 3.30"


def test_parse_regular_shift():
    text = "10 Lynnwood 7.00 - 1.30 6.5h"

    result = parse_entry(text)

    assert result is not None
    assert result.date == "10"
    assert result.city == "Lynnwood"
    assert result.start == "7:00"
    assert result.end == "1:30"
    assert result.hours == 6.5
    assert result.prevailing_hours is None


def test_parse_shift_with_prevailing_hours():
    text = "10 Linwood 7.00 - 1.30 6.5h " "Prevailing hours: 8.00 - 11.30 3.5h"

    result = parse_entry(text)

    assert result is not None
    assert result.date == "10"
    assert result.city == "Linwood"
    assert result.start == "7:00"
    assert result.end == "1:30"
    assert result.hours == 6.5
    assert result.prevailing_hours == 3.5


def test_parse_multiline_entry():
    text = """
    20 Lynnwood
    6.00 - 3.30 9.5h
    Prevailing hours: 7.00 - 1.30 6.5h
    """

    result = parse_entry(text)

    assert result is not None
    assert result.date == "20"
    assert result.city == "Lynnwood"
    assert result.start == "6:00"
    assert result.end == "3:30"
    assert result.hours == 9.5
    assert result.prevailing_hours == 6.5


def test_parse_timesheet():
    text = """
    1/03 Kirkland 8.00 - 3.00 7h

    3/03 Whidbey, Ferndale 6.00 - 5.30 11.5h

    4/03 Whidbey, Ferndale 6.30 - 1.00 6.5h
    """

    result = parse_timesheet(text)

    assert len(result) == 3

    assert result[0].city == "Kirkland"
    assert result[0].hours == 7.0

    assert result[1].city == "Whidbey, Ferndale"
    assert result[1].hours == 11.5

    assert result[2].city == "Whidbey, Ferndale"
    assert result[2].hours == 6.5


def test_invalid_entry_returns_none():
    text = "This is not a valid timesheet entry"

    result = parse_entry(text)

    assert result is None
