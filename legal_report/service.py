from datetime import date
from pathlib import Path

from .infrai_client import send_email
from .models import MatterIntake
from .pdf_report import report_text, write_pdf


def deliver_report(matter: MatterIntake, output: Path, today: date | None = None) -> dict:
    run_date = today or date.today()
    body = report_text(matter, run_date)
    write_pdf(matter, run_date, output)
    return send_email({"to": matter.recipient, "subject": f"Matter report {matter.matter_id}", "body": body})
