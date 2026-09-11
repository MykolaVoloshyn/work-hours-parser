from dataclasses import dataclass


@dataclass
class WorkShift:
    date: str
    start: str
    end: str
    city: str
    hours: float
    prevailing_hours: float | None = None
