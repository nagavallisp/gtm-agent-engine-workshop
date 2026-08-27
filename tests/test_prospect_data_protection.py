import json
import os
import unittest
from unittest.mock import patch

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ["LANGSMITH_TRACING"] = "false"

from gtm_agent import gtm_agent
from gtm_agent import data_service


class _ScoringResult:
    def model_dump(self):
        return {"score": 80}


class ProspectDataProtectionTests(unittest.TestCase):
    def setUp(self):
        data_service._PROFILES.clear()

    def test_sensitive_fields_are_excluded_from_prospect_outputs_and_prompt(self):
        prospect_id = "LEAD-90001"
        offering = data_service.get_offering("OFFER-10007")

        prospect = gtm_agent.get_prospect.invoke({"prospect_id": prospect_id})
        profile = gtm_agent.build_prospect_profile.invoke({"prospect_id": prospect_id})
        scoring_llm = unittest.mock.Mock(invoke=unittest.mock.Mock(return_value=_ScoringResult()))
        with patch.object(gtm_agent, "_scoring_llm", scoring_llm):
            gtm_agent.score_prospect.invoke({
                "prospect_profile": profile["prospect_profile"],
                "offering": offering,
            })

        forbidden = ("tax_id", "card_on_file", "date_of_birth", "credit_check_ref")
        self.assertFalse(any(key in json.dumps(prospect) for key in forbidden))
        self.assertFalse(any(key in json.dumps(profile) for key in forbidden))
        prompt = scoring_llm.invoke.call_args.args[0][1]["content"]
        self.assertFalse(any(key in prompt for key in forbidden))


if __name__ == "__main__":
    unittest.main()
