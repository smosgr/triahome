from app.ai import is_property_issue, diagnose_property_issue


from app.ai import is_property_issue


def test_property_issue_gate_accepts_plumbing_problem():
    assert is_property_issue(
        "The pipe under my kitchen sink is leaking."
    ) is True


def test_property_issue_gate_accepts_heating_problem():
    assert is_property_issue(
        "My radiator is not getting warm."
    ) is True


def test_property_issue_gate_rejects_cv_request():
    assert is_property_issue(
        "Can you write a CV for me?"
    ) is False


def test_property_issue_gate_rejects_unrelated_question():
    assert is_property_issue(
        "What is the capital of France?"
    ) is False


def test_property_issue_gate_rejects_unrelated_question_gr():
    assert is_property_issue(
        "Ti kanei niaou niaou sta keramidia?"
    ) is False

def test_diagnosis_uses_user_description():
    description = "The pipe under my kitchen sink is leaking."

    result = diagnose_property_issue(description)

    assert result["problem"]["summary"] == description