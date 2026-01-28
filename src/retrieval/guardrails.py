def validate_response(response_text):
    """
    Validates the response to ensure it adheres to guardrails.
    (Currently mostly handled by system prompt, but this is a placeholder for post-processing if needed)
    """
    # Helper to enforce the exact "I don't have enough information..." string if the model indicates uncertainty in a different way
    # For now, we rely on the prompt, but we could add checks here.
    return response_text

def check_hallucination_guardrails(question):
    """
    Pre-checks or post-checks for hallucination triggers.
    Week 2 requirement: "Topic is unrelated", "Public figures / current events".
    Implementation:
    In a real system, we might use a classifier. 
    Here, the prompt "Answer only using the retrieved context" is the primary mechanism.
    However, if we retrieved documents that are irrelevant, the model should say "I don't have enough information...".
    """
    pass
