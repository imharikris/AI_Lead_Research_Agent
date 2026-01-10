def validator_node(state: dict) -> dict:
    email = state.get("email_draft", "")
    retries = state.get("email_retry", 0)

    if len(email.split()) < 50:
        if retries >= 1:
            state["email_valid"] = True
            state["email_draft"] = f"FAILED_QUALITY: {email}"
            return state

        state["email_valid"] = False
        state["email_retry"] = retries + 1
        return state

    state["email_valid"] = True
    return state