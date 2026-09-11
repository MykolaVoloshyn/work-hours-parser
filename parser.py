import logging
import re

from models import WorkShift


logger = logging.getLogger(__name__)


MAIN_PATTERN = re.compile(
    r"(?P<date>\d{1,2}/?\d{0,2})\s+"
    r"(?P<city>.+?)\s+"
    r"(?P<start>\d{1,2}\.\d{2})\s*-\s*"
    r"(?P<end>\d{1,2}\.\d{2})\s+"
    r"(?P<hours>\d+\.?\d*)h"
)


PREVAILING_PATTERN = re.compile(
    r"Prevailing hours:\s*" r"\d{1,2}\.\d{2}\s*-\s*" r"\d{1,2}\.\d{2}\s+" r"(?P<hours>\d+\.?\d*)h"
)


def normalize_whitespace(text: str) -> str:
    """Replace multiple whitespace characters with a single space."""
    return re.sub(r"\s+", " ", text).strip()


def parse_entry(entry: str) -> WorkShift | None:
    """
    Parse one timesheet entry.

    Returns WorkShift if parsing succeeds,
    otherwise returns None.
    """

    entry = normalize_whitespace(entry)

    # Find prevailing hours
    prevailing_match = PREVAILING_PATTERN.search(entry)

    prevailing_hours = None

    if prevailing_match:
        prevailing_hours = float(prevailing_match.group("hours"))

        # Remove prevailing hours from the entry
        entry = PREVAILING_PATTERN.sub("", entry).strip()

    # Parse main shift
    match = MAIN_PATTERN.match(entry)

    if not match:
        logger.warning("Could not parse entry: %s", entry)
        return None

    return WorkShift(
        date=match.group("date"),
        start=match.group("start").replace(".", ":"),
        end=match.group("end").replace(".", ":"),
        city=match.group("city"),
        hours=float(match.group("hours")),
        prevailing_hours=prevailing_hours,
    )


def parse_timesheet(text: str) -> list[WorkShift]:
    """
    Parse complete timesheet text.

    Entries are separated by empty lines.
    """

    entries = text.split("\n\n")

    shifts: list[WorkShift] = []

    for entry in entries:
        if not entry.strip():
            continue

        shift = parse_entry(entry)

        if shift is not None:
            shifts.append(shift)

    logger.info("Successfully parsed %d shifts", len(shifts))

    return shifts


def read_input_file(path: str) -> str:
    """Read input text file."""

    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError:
        logger.error("Input file not found: %s", path)
        raise

    except PermissionError:
        logger.error("Permission denied: %s", path)
        raise
