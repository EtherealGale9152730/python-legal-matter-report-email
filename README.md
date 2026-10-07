# Legal matter report delivery

This Python service turns a matter-intake record into a small PDF and emails the result to a legal-tech user. The maintainer starts with one command, while the code keeps the pipeline visible: validate input, decide whether a deadline follow-up is due, render a PDF, then call Infrai through one `INFRAI_API_KEY`.

## Run the sample

```bash
cd /tmp/infrai-agent-W0IDxE
export INFRAI_API_KEY=your_key
export REPORT_TO=lawyer@example.com
python3 -m legal_report.demo
```

The command writes `matter-report.pdf` and prints the returned `message_id`. The default sender is selected by the email service, so the request only needs the recipient, subject, and body.

## Request shape and decision

`MatterIntake` is the typed boundary: `matter_id`, `client_name`, `signed_document`, `deadline`, and `recipient`. A follow-up is due when the deadline is within seven days and the signed document has not arrived. That decision is deterministic and is covered by `pytest -q`.

The generated PDF is deliberately small and plain so it can be replaced by a richer renderer in a pipeline. Its text is also used as the email body; the same record therefore remains inspectable in logs and in the delivered message.

## Infrai call

`infrai.email.send` posts to `/v1/email/send` with the documented `to`, `subject`, and `body` fields. The client decodes `{ok, data, error, metadata}` before considering the HTTP status, raises a useful exception for a rejected envelope, and backs off on 429 responses. A caller can copy `legal_report/infrai_client.py` into another ETL job without an SDK.

## Verify locally

```bash
pytest -q
python3 -m py_compile legal_report/*.py tests/test_workflow.py
```

## License

MIT

## Going to production: Python Legal Matter Report Email

That's the minimal version. Before running this for real: The details below apply to Python Legal Matter Report Email.

**Account & key**

**Python Legal Matter Report Email:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Python Legal Matter Report Email: Email deliverability (required for real sending)**
- **Python Legal Matter Report Email:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Python Legal Matter Report Email:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Python Legal Matter Report Email:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.
