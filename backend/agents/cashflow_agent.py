# ============================================================
# RECOVERAI
# CASH-FLOW INTELLIGENCE AGENT
# ============================================================


# Demo merchant starting cash balance.
#
# This is a configurable demo value for the hackathon.
# In a production system this would come from the
# merchant's accounting/payment data.
STARTING_CASH = 210000.0


# ============================================================
# RECOVERY PROBABILITY
# ============================================================

def calculate_recovery_probability(transaction, action):

    successes = int(
        transaction.get(
            "previous_successes",
            0
        )
    )

    failures = int(
        transaction.get(
            "previous_failures",
            0
        )
    )

    total_history = successes + failures

    if total_history > 0:

        historical_success_rate = (
            successes / total_history
        )

    else:

        historical_success_rate = 0.30


    # Action-specific adjustment

    if action == "RETRY":

        probability = (
            historical_success_rate
        )

    elif action == "REMIND":

        probability = (
            historical_success_rate * 0.75
        )

    elif action == "ESCALATE":

        probability = (
            historical_success_rate * 0.65
        )

    elif action == "INCENTIVE":

        probability = (
            historical_success_rate * 0.85
        )

    else:

        probability = 0.0


    # Keep probability between 5% and 95%

    if action != "STOP":

        probability = max(
            0.05,
            min(
                probability,
                0.95
            )
        )

    return round(
        probability,
        3
    )


# ============================================================
# CASH-FLOW INTELLIGENCE
# ============================================================

def analyze_cashflow(transactions):

    from backend.agents.recovery_agent import (
        choose_recovery_action
    )


    # ========================================================
    # STARTING CASH
    # ========================================================

    current_cash = STARTING_CASH


    # ========================================================
    # EXPECTED RECOVERY
    # ========================================================

    expected_recovery = 0.0

    recovery_details = []


    # ========================================================
    # PROCESS TRANSACTIONS
    # ========================================================

    for transaction in transactions:

        amount = float(
            transaction.get(
                "amount",
                0
            )
        )

        status = str(
            transaction.get(
                "status",
                ""
            )
        ).lower()


        # Only revenue-at-risk transactions

        if status not in [
            "failed",
            "abandoned",
            "overdue"
        ]:

            continue


        # ----------------------------------------------------
        # Recovery Agent
        # ----------------------------------------------------

        decision = choose_recovery_action(
            transaction
        )


        action = decision.get(
            "action",
            "STOP"
        )


        # ----------------------------------------------------
        # Recovery probability
        # ----------------------------------------------------

        probability = (
            calculate_recovery_probability(
                transaction,
                action
            )
        )


        # ----------------------------------------------------
        # Expected recovery
        # ----------------------------------------------------

        expected_amount = (
            amount * probability
        )


        expected_recovery += (
            expected_amount
        )


        recovery_details.append({

            "transaction_id": (
                transaction.get(
                    "transaction_id"
                )
            ),

            "amount": amount,

            "action": action,

            "recovery_probability": (
                probability
            ),

            "expected_recovery": round(
                expected_amount,
                2
            ),

            "reason": decision.get(
                "reason",
                ""
            )
        })


    # ========================================================
    # TOTAL EXPECTED RECOVERY
    # ========================================================

    expected_recovery = round(
        expected_recovery,
        2
    )


    # ========================================================
    # 7-DAY PROJECTED CASH
    # ========================================================

    projected_cash_7_days = round(
        current_cash
        +
        expected_recovery,
        2
    )


    # ========================================================
    # CASH IMPROVEMENT
    # ========================================================

    cash_position_improvement = round(
        projected_cash_7_days
        -
        current_cash,
        2
    )


    # ========================================================
    # DAILY FORECAST
    # ========================================================

    daily_expected_recovery = round(
        expected_recovery / 7,
        2
    )


    forecast = []


    for day in range(1, 8):

        projected_cash = round(
            current_cash
            +
            (
                daily_expected_recovery
                * day
            ),
            2
        )

        forecast.append({

            "day": day,

            "projected_cash": (
                projected_cash
            )
        })


    # ========================================================
    # RETURN
    # ========================================================

    return {

        "current_cash": round(
            current_cash,
            2
        ),

        "expected_recovery": (
            expected_recovery
        ),

        "projected_cash_7_days": (
            projected_cash_7_days
        ),

        "cash_position_improvement": (
            cash_position_improvement
        ),

        "total_recovery_opportunities": (
            len(recovery_details)
        ),

        "recovery_opportunities": (
            recovery_details
        ),

        "forecast": forecast
    }