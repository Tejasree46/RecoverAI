def execute_payment_action(transaction, decision, guardrail):

    transaction_id = transaction.get(
        "transaction_id",
        transaction.get("id", "UNKNOWN")
    )

    action = decision.get(
        "action",
        "STOP"
    )

    # =========================================================
    # 1. GUARDRAIL BLOCKED
    # =========================================================

    if not guardrail.get("allowed", False):

        return {
            "transaction_id": transaction_id,
            "action": action,
            "status": "PENDING_APPROVAL",
            "executed": False,
            "message": guardrail.get(
                "reason",
                "Human approval required."
            )
        }

    # =========================================================
    # 2. HUMAN-APPROVED ESCALATION
    # =========================================================

    if action == "ESCALATE":

        # Extra safety check:
        # ESCALATE can execute only when human approval
        # was explicitly recorded.

        if guardrail.get("human_approved") is True:

            return {
                "transaction_id": transaction_id,
                "action": action,
                "status": "EXECUTED",
                "executed": True,
                "message": (
                    "Human approval received. "
                    "Escalated recovery action executed "
                    "in Razorpay test mode."
                )
            }

        return {
            "transaction_id": transaction_id,
            "action": action,
            "status": "PENDING_APPROVAL",
            "executed": False,
            "message": (
                "ESCALATE requires explicit human approval."
            )
        }

    # =========================================================
    # 3. RETRY PAYMENT
    # =========================================================

    if action == "RETRY":

        return {
            "transaction_id": transaction_id,
            "action": action,
            "status": "EXECUTED",
            "executed": True,
            "message": (
                "Payment retry initiated "
                "in Razorpay test mode."
            )
        }

    # =========================================================
    # 4. SEND REMINDER
    # =========================================================

    if action == "REMIND":

        return {
            "transaction_id": transaction_id,
            "action": action,
            "status": "EXECUTED",
            "executed": True,
            "message": (
                "Payment reminder sent "
                "in test mode."
            )
        }

    # =========================================================
    # 5. STOP
    # =========================================================

    if action == "STOP":

        return {
            "transaction_id": transaction_id,
            "action": action,
            "status": "STOPPED",
            "executed": False,
            "message": (
                "No recovery action required."
            )
        }

    # =========================================================
    # 6. UNKNOWN ACTION
    # =========================================================

    return {
        "transaction_id": transaction_id,
        "action": action,
        "status": "PENDING_APPROVAL",
        "executed": False,
        "message": (
            "Unknown action requires human approval."
        )
    }