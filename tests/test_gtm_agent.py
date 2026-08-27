import os
from types import SimpleNamespace

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from gtm_agent.gtm_agent import send_prospect_email


def test_send_prospect_email_blocks_disqualified_prospect_without_override():
    prospect = {
        "prospect_id": "LEAD-50001",
        "name": "Priya Nair",
        "email": "priya.nair@brightwaveapps.com",
    }
    runtime = SimpleNamespace(config={"metadata": {}})

    blocked = send_prospect_email.func(
        prospect, "Invitation to Book a Demo", "Please book a demo.", runtime
    )
    sent = send_prospect_email.func(
        prospect,
        "Invitation to Book a Demo",
        "Please book a demo.",
        runtime,
        override_disqualified=True,
    )

    assert blocked == {"status": "blocked", "reason": "prospect is disqualified"}
    assert sent["status"] == "sent"
