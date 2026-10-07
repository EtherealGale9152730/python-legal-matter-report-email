from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class MatterIntake:
    matter_id: str
    client_name: str
    signed_document: bool
    deadline: date
    recipient: str


def follow_up_due(matter: MatterIntake, today: date) -> bool:
    days_left = (matter.deadline - today).days
    return not matter.signed_document and 0 <= days_left <= 7
