def check_guardrail(transaction, action):

    amount = transaction["amount"]

    # High-value transactions need human approval
    if amount >= 30000:
        return {
            "allowed": False,
            "approval_required": True,
            "reason": "High-value transaction requires human approval."
        }

    # Escalation always requires human approval
    if action == "ESCALATE":
        return {
            "allowed": False,
            "approval_required": True,
            "reason": "Escalation requires human approval."
        }

    # Retry is allowed for normal transactions
    if action == "RETRY":
        return {
            "allowed": True,
            "approval_required": False,
            "reason": "Retry is allowed within the transaction limit."
        }

    # Reminder is safe to execute
    if action == "REMIND":
        return {
            "allowed": True,
            "approval_required": False,
            "reason": "Reminder is a low-risk recovery action."
        }

    # Stop means no action
    if action == "STOP":
        return {
            "allowed": True,
            "approval_required": False,
            "reason": "No recovery action is required."
        }

    # Anything unknown is blocked
    return {
        "allowed": False,
        "approval_required": True,
        "reason": "Unknown action requires manual approval."
    }