from pathlib import Path

from .models import MatterIntake, follow_up_due


def report_text(matter: MatterIntake, today) -> str:
    status = "follow-up due" if follow_up_due(matter, today) else "no follow-up"
    return (
        f"Matter: {matter.matter_id}\n"
        f"Client: {matter.client_name}\n"
        f"Signed document: {'received' if matter.signed_document else 'pending'}\n"
        f"Deadline: {matter.deadline.isoformat()}\n"
        f"Decision: {status}\n"
    )


def write_pdf(matter: MatterIntake, today, destination: Path) -> str:
    text = report_text(matter, today)
    stream = f"BT /F1 12 Tf 72 740 Td ({text.replace(chr(10), ') Tj 0 -18 Td (' )}) Tj ET"
    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        f"<< /Length {len(stream.encode())} >>\nstream\n{stream}\nendstream",
    ]
    pdf = "%PDF-1.4\n"; offsets = [0]
    for index, obj in enumerate(objects, 1):
        offsets.append(len(pdf.encode()))
        pdf += f"{index} 0 obj\n{obj}\nendobj\n"
    xref = len(pdf.encode())
    pdf += "xref\n0 6\n0000000000 65535 f \n" + "".join(f"{n:010d} 00000 n \n" for n in offsets[1:])
    pdf += f"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    destination.write_bytes(pdf.encode())
    return text
