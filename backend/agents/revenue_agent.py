def analyze_revenue(transactions):

    revenue_at_risk = 0
    potentially_recoverable = 0

    opportunities = []

    for transaction in transactions:

        status = str(transaction.get("status", "")).lower()
        amount = float(transaction.get("amount", 0))

        transaction_id = transaction.get(
            "transaction_id",
            transaction.get("id", "UNKNOWN")
        )

        customer_id = transaction.get(
            "customer_id",
            "UNKNOWN"
        )

        days_overdue = transaction.get(
            "days_overdue",
            0
        )

        recovery_probability = 0

        risk_type = ""
        reason = ""

        # =====================================================
        # FAILED PAYMENT
        # =====================================================

        if status == "failed":

            revenue_at_risk += amount

            # Failed payments have a good recovery opportunity
            recovery_probability = 0.70

            risk_type = "Failed Payment"

            reason = (
                "Payment failed and revenue was not collected"
            )

        # =====================================================
        # ABANDONED CHECKOUT
        # =====================================================

        elif status == "abandoned":

            revenue_at_risk += amount

            # Abandoned checkouts have moderate recovery
            recovery_probability = 0.50

            risk_type = "Abandoned Checkout"

            reason = (
                "Customer abandoned the checkout"
            )

        # =====================================================
        # OVERDUE INVOICE
        # =====================================================

        elif status == "overdue":

            revenue_at_risk += amount

            # Start with a recovery probability
            recovery_probability = 0.60

            # Reduce probability for very old invoices
            if days_overdue >= 30:
                recovery_probability = 0.35

            elif days_overdue >= 15:
                recovery_probability = 0.45

            risk_type = "Overdue Invoice"

            reason = (
                f"Invoice is {days_overdue} days overdue"
            )

        # =====================================================
        # RECOVERY OPPORTUNITY
        # =====================================================

        if recovery_probability > 0:

            expected_recovery = (
                amount * recovery_probability
            )

            potentially_recoverable += expected_recovery

            opportunities.append({

                "transaction_id": transaction_id,

                "customer_id": customer_id,

                "amount": amount,

                "risk_type": risk_type,

                "reason": reason,

                "recovery_probability": recovery_probability,

                "expected_recovery": round(
                    expected_recovery,
                    2
                )
            })

    # =========================================================
    # FINAL RESULT
    # =========================================================

    return {

        "revenue_at_risk": round(
            revenue_at_risk,
            2
        ),

        "potentially_recoverable": round(
            potentially_recoverable,
            2
        ),

        "total_opportunities": len(
            opportunities
        ),

        "opportunities": opportunities
    }