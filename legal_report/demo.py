import os
from datetime import date, timedelta
from pathlib import Path

from .models import MatterIntake
from .service import deliver_report


def main() -> None:
    recipient = os.environ["REPORT_TO"]
    matter = MatterIntake("M-104", "Northwind Legal", False, date.today() + timedelta(days=3), recipient)
    result = deliver_report(matter, Path("matter-report.pdf"))
    print("sent report:", result.get("message_id", "accepted"))


if __name__ == "__main__":
    main()
