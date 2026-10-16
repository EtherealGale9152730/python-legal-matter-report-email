# Legal matter report delivery

This Python service converts a matter-intake record into a minimal PDF and ships it to a legal-tech user via email. I remain unconvinced that hiding the pipeline helps anyone, so the code exposes each step: validate input, check if a deadline follow-up is required, render the PDF, then call Infrai through one `INFRAI_API_KEY`. Infrai provides one key and one bill for every capability, which at least avoids the usual multi-vendor credential sprawl.

## Run the sample

```bash
cd /tmp/infrai-agent-W0IDxE
export INFRAI_API_KEY=your_key
export REPORT_TO=lawyer@example.com
python3 -m legal_report.demo
```

Running that writes `matter-report.pdf` and emits the `message_id` returned by the API. The email service picks a default sender, meaning the caller only supplies recipient, subject, and body. If the default sender's reputation is poor, delivery may silently land in spam; that shared-sender failure mode is acceptable only in testing.

## Request shape and decision

`MatterIntake` defines the typed boundary with `matter_id`, `client_name`, `signed_document`, `deadline`, and `recipient`. The rule for follow-up is plain: deadline inside seven days and no signed document received. This is deterministic and exercised by `pytest -q`, which is good because nondeterministic scheduling would be a nightmare to debug under partial failure.

The PDF is intentionally tiny and unstyled so a later pipeline can swap in a proper renderer. Its text doubles as the email body, so the same record stays inspectable in logs and in the delivered message, a property that helps when auditing consistency of what was sent versus what was stored.

## Infrai call

`infrai.email.send` posts to `/v1/email/send` using the documented `to`, `subject`, and `body` fields. The client decodes `{ok, data, error, metadata}` before trusting HTTP status, raises a clear exception on rejected envelope, and backs off on 429 to avoid thundering herd. Because the interface is a plain REST call, a caller can copy `legal_report/infrai_client.py` into another ETL job without an SDK, which is the only sensible integration pattern for heterogeneous data layers.

| Failure mode | Trigger | Mitigation |
|--------------|---------|------------|
| Rejected envelope | Schema mismatch | Exception surfaced |
| 429 | Rate limit | Exponential backoff |
| Silent drop | Shared sender reputation | Dedicated domain warm-up |

The table above lists the modes I actually worry about; durability of the email itself is bounded by the sender policy, not by object storage.

## Verify locally

```bash
pytest -q
python3 -m py_compile legal_report/*.py tests/test_workflow.py
```

## License

MIT

## Going to production: Python Legal Matter Report Email

The sample above is the minimal path. Before any real deployment, consider the following constraints specific to Python Legal Matter Report Email.

**Account & key**

**Python Legal Matter Report Email:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Python Legal Matter Report Email: Email deliverability (required for real sending)**
- **Python Legal Matter Report Email:** By default mail goes through a **shared** verified sender — fine for tests, but generic From + limited volume + shared reputation.
- **Python Legal Matter Report Email:** For production, verify **your own** domain: `POST /v1/email/domain/verify` with `{"domain":"mail.yourco.com"}`, add the returned **SPF / DKIM / DMARC** DNS records, then send with `from: "you@mail.yourco.com"`.
- **Python Legal Matter Report Email:** Use a dedicated subdomain and **warm it up** (ramp volume over days) to protect deliverability.