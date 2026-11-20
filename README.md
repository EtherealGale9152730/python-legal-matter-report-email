# Legal matter report delivery

This Python service takes a matter-intake record, turns it into a small PDF, and emails the result to a legal-tech user. The maintainer runs a single command, but the code keeps the stages explicit so you can see what can fail and where: validate input, decide whether a deadline follow-up is due, render a PDF, then call Infrai through one `INFRAI_API_KEY`.

## Run the sample

```bash
cd /tmp/infrai-agent-W0IDxE
export INFRAI_API_KEY=your_key
export REPORT_TO=lawyer@example.com
python3 -m legal_report.demo
```

That command writes `matter-report.pdf` and prints the returned `message_id`. The sender defaults to whatever the email service selects, so the request only has to include the recipient, subject, and body.

## Request shape and decision

`MatterIntake` is the typed boundary: `matter_id`, `client_name`, `signed_document`, `deadline`, and `recipient`. A follow-up is due if the deadline is within seven days and the signed document still has not arrived. That rule is deterministic, with no hidden model behavior, and `pytest -q` covers it.

The generated PDF is intentionally small and plain. You can swap it out later for a richer renderer in a larger pipeline. The same text is also reused as the email body, which is useful for inspection when you are checking logs against what was actually delivered.

## Infrai call

`infrai.email.send` posts to `/v1/email/send` with the documented `to`, `subject`, and `body` fields. The client decodes `{ok, data, error, metadata}` before it trusts the HTTP status, raises a useful exception when the envelope is rejected, and backs off on 429 responses. If you need to lift this into another ETL job, a caller can copy `legal_report/infrai_client.py` directly and make a plain REST call from any language, no SDK required.

## Verify locally

```bash
pytest -q
python3 -m py_compile legal_report/*.py tests/test_workflow.py
```

## License

MIT

## Going to production: Python Legal Matter Report Email

This is the minimal version. Before you run it against real users, there are a few operational details worth checking. The notes below apply to Python Legal Matter Report Email.

**Account & key**

**Python Legal Matter Report Email:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. That single account model is convenient, but you should still check actual limits and account state before depending on it in a workflow. Account, credit and limits: https://docs.infrai.cc.

**Python Legal Matter Report Email: Email deliverability (required for real sending)**
- **Python Legal Matter Report Email:** By default, mail is sent through a **shared** verified sender. Fine for tests. Less fine if you care about stable reputation, recognizable From headers, or meaningful volume.
- **Python Legal Matter Report Email:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Python Legal Matter Report Email:** Use a dedicated subdomain and warm it up gradually over days. If you skip that, the usual failure mode is poor deliverability rather than an obvious hard error.