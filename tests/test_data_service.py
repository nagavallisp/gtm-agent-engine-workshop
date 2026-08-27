from gtm_agent import data_service


def test_update_prospect_info_persists_technology_and_invalidates_profile():
    prospect_id = next(iter(data_service.PROSPECTS))
    original_stack = list(data_service.PROSPECTS[prospect_id]["tech_stack"])
    data_service.save_profile_to_db(
        prospect_id,
        {"prospect_id": prospect_id, "tech_stack": original_stack},
    )

    try:
        result = data_service.update_prospect_info(prospect_id, "Terraform")

        assert result["updated"] is True
        assert "Terraform" in data_service.fetch_tech_stack(prospect_id)
        assert data_service.get_profile_from_db(prospect_id)["prospect_profile"] is None

        rebuilt_profile = {
            "prospect_id": prospect_id,
            "tech_stack": data_service.fetch_tech_stack(prospect_id),
        }
        data_service.save_profile_to_db(prospect_id, rebuilt_profile)
        assert "Terraform" in data_service.get_profile_from_db(prospect_id)[
            "prospect_profile"
        ]["tech_stack"]
    finally:
        data_service.PROSPECTS[prospect_id]["tech_stack"] = original_stack
        data_service._PROFILES.pop(prospect_id, None)
