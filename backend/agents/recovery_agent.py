def choose_recovery_action(transaction):

    status = transaction["status"]
    amount = transaction["amount"]

    previous_successes = transaction["previous_successes"]
    previous_failures = transaction["previous_failures"]

    days_overdue = transaction["days_overdue"]

    # Failed payment
    if status == "failed":

        # Customer has a strong payment history
        if previous_successes >= 5 and previous_failures <= 2:
            action = "RETRY"
            reason = "Customer has a strong previous payment history."

        # Large amount with poor payment history
        elif amount >= 30000 and previous_failures >= 3:
            action = "ESCALATE"
            reason = "High-value transaction with poor payment history."

        else:
            action = "REMIND"
            reason = "Payment failed and customer should be reminded."

    # Abandoned checkout
    elif status == "abandoned":

        if amount >= 20000:
            action = "REMIND"
            reason = "High-value abandoned checkout requires customer follow-up."

        else:
            action = "REMIND"
            reason = "Customer abandoned checkout and should be reminded."

    # Overdue invoice
    elif status == "overdue":

        if days_overdue >= 15:
            action = "ESCALATE"
            reason = "Invoice is significantly overdue."

        else:
            action = "REMIND"
            reason = "Invoice is overdue and customer should be reminded."

    else:
        action = "STOP"
        reason = "No recovery action is required."

    return {
        "transaction_id": transaction["transaction_id"],
        "customer_id": transaction["customer_id"],
        "amount": amount,
        "action": action,
        "reason": reason
    }