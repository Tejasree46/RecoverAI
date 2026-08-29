from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.database import load_transactions

from backend.agents.revenue_agent import (
    analyze_revenue
)

from backend.agents.recovery_agent import (
    choose_recovery_action
)

from backend.utils.guardrails import (
    check_guardrail
)

from backend.agents.payment_agent import (
    execute_payment_action
)

from backend.agents.cashflow_agent import (
    analyze_cashflow
)

from backend.approval_database import (
    initialize_approval_database,
    save_approval,
    get_approval,
    get_all_approvals
)


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="RecoverAI",
    description=(
        "AI-powered Revenue Recovery and "
        "Cash-Flow Intelligence Platform"
    ),
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# APPROVAL REQUEST
# ============================================================

class ApprovalRequest(BaseModel):

    transaction_id: str

    approved: bool


# ============================================================
# START DATABASE
# ============================================================

initialize_approval_database()


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "project": "RecoverAI",

        "status": "running",

        "message": (
            "Revenue Recovery Agent "
            "is online!"
        )
    }


# ============================================================
# TRANSACTIONS
# ============================================================

@app.get("/transactions")
def get_transactions():

    df = load_transactions()

    transactions = df.to_dict(
        orient="records"
    )

    return {
        "total_transactions":
            len(transactions),

        "transactions":
            transactions
    }


# ============================================================
# REVENUE ANALYSIS
# ============================================================

@app.get("/revenue-analysis")
def revenue_analysis():

    df = load_transactions()

    transactions = df.to_dict(
        orient="records"
    )

    return analyze_revenue(
        transactions
    )


# ============================================================
# RECOVERY ANALYSIS
# ============================================================

@app.get("/recovery-analysis")
def recovery_analysis():

    df = load_transactions()

    transactions = df.to_dict(
        orient="records"
    )

    decisions = []

    for transaction in transactions:

        decision = choose_recovery_action(
            transaction
        )

        decisions.append({

            "transaction":
                transaction,

            "decision":
                decision
        })

    return {

        "total_transactions":
            len(transactions),

        "recovery_decisions":
            decisions
    }


# ============================================================
# CASH FLOW
# ============================================================

@app.get("/cashflow-forecast")
def cashflow_forecast():

    df = load_transactions()

    transactions = df.to_dict(
        orient="records"
    )

    return analyze_cashflow(
        transactions
    )


# ============================================================
# HELPER
# ============================================================

def get_transaction_id(transaction):

    return (
        transaction.get("transaction_id")
        or
        transaction.get("id")
    )


# ============================================================
# HUMAN APPROVAL
#
# FRONTEND
#       ↓
# POST /approval
#       ↓
# SQLite
#       ↓
# Dashboard
# ============================================================

@app.post("/approval")
def process_approval(
    request: ApprovalRequest
):

    transaction_id = request.transaction_id

    approved = request.approved


    # --------------------------------------------------------
    # LOAD TRANSACTIONS
    # --------------------------------------------------------

    df = load_transactions()

    transactions = df.to_dict(
        orient="records"
    )


    # --------------------------------------------------------
    # FIND TRANSACTION
    # --------------------------------------------------------

    transaction = None

    for item in transactions:

        item_id = get_transaction_id(
            item
        )

        if item_id == transaction_id:

            transaction = item

            break


    # --------------------------------------------------------
    # NOT FOUND
    # --------------------------------------------------------

    if transaction is None:

        raise HTTPException(

            status_code=404,

            detail=(
                f"Transaction "
                f"{transaction_id} not found."
            )
        )


    # --------------------------------------------------------
    # AI DECISION
    # --------------------------------------------------------

    decision = choose_recovery_action(
        transaction
    )

    action = decision.get(
        "action",
        "STOP"
    )


    # ========================================================
    # REJECT
    # ========================================================

    if not approved:

        status = "REJECTED"

        message = (
            "Recovery action rejected "
            "by human reviewer."
        )


        # SAVE DECISION

        save_approval(

            transaction_id,

            False,

            status,

            action,

            message
        )


        guardrail = {

            "allowed":
                False,

            "approval_required":
                False,

            "human_approved":
                False,

            "status":
                "REJECTED",

            "reason":
                message
        }


        execution = {

            "transaction_id":
                transaction_id,

            "action":
                action,

            "status":
                "REJECTED",

            "executed":
                False,

            "message":
                message
        }


        return {

            "transaction_id":
                transaction_id,

            "approval":
                "REJECTED",

            "status":
                "REJECTED",

            "executed":
                False,

            "action":
                action,

            "guardrail":
                guardrail,

            "execution":
                execution
        }


    # ========================================================
    # APPROVE
    # ========================================================

    status = "EXECUTED"

    message = (
        "Human approval received. "
        "Action authorized for "
        "test execution."
    )


    # SAVE DECISION

    save_approval(

        transaction_id,

        True,

        status,

        action,

        message
    )


    guardrail = {

        "allowed":
            True,

        "approval_required":
            False,

        "human_approved":
            True,

        "status":
            "APPROVED",

        "reason":
            message
    }


    # --------------------------------------------------------
    # ESCALATED ACTION
    # --------------------------------------------------------

    if action == "ESCALATE":

        execution = {

            "transaction_id":
                transaction_id,

            "action":
                action,

            "status":
                "EXECUTED",

            "executed":
                True,

            "message":
                (
                    "Human approval received. "
                    "Escalated recovery action "
                    "executed in Razorpay "
                    "test mode."
                )
        }


    # --------------------------------------------------------
    # NORMAL PAYMENT ACTION
    # --------------------------------------------------------

    else:

        execution = execute_payment_action(

            transaction,

            decision,

            guardrail
        )


    return {

        "transaction_id":
            transaction_id,

        "approval":
            "APPROVED",

        "status":
            "EXECUTED",

        "executed":
            True,

        "action":
            action,

        "guardrail":
            guardrail,

        "execution":
            execution
    }


# ============================================================
# EXECUTE RECOVERY AGENT
#
# IMPORTANT:
# Supports BOTH GET and POST.
#
# This prevents the 405 problem from the Run Recovery
# Agent button.
# ============================================================

@app.get("/execute-recovery")
@app.post("/execute-recovery")
def execute_recovery():

    df = load_transactions()

    transactions = df.to_dict(
        orient="records"
    )


    executed = []

    pending = []

    rejected = []


    # ========================================================
    # PROCESS EVERY TRANSACTION
    # ========================================================

    for transaction in transactions:

        transaction_id = get_transaction_id(
            transaction
        )

        if not transaction_id:
            continue


        # ----------------------------------------------------
        # AI DECISION
        # ----------------------------------------------------

        decision = choose_recovery_action(
            transaction
        )

        action = decision.get(
            "action",
            "STOP"
        )


        # ----------------------------------------------------
        # CHECK PREVIOUS HUMAN DECISION
        # ----------------------------------------------------

        saved_approval = get_approval(
            transaction_id
        )


        # ====================================================
        # ALREADY REJECTED
        # ====================================================

        if (
            saved_approval
            and
            saved_approval.get("status")
            == "REJECTED"
        ):

            rejected.append({

                "transaction_id":
                    transaction_id,

                "action":
                    action,

                "status":
                    "REJECTED",

                "executed":
                    False,

                "message":
                    (
                        "Recovery action rejected "
                        "by human reviewer."
                    )
            })

            continue


        # ====================================================
        # ALREADY APPROVED
        # ====================================================

        if (
            saved_approval
            and
            saved_approval.get("status")
            == "EXECUTED"
        ):

            executed.append({

                "transaction_id":
                    transaction_id,

                "action":
                    action,

                "status":
                    "EXECUTED",

                "executed":
                    True,

                "message":
                    (
                        "Human approval already "
                        "received. Recovery action "
                        "is authorized."
                    )
            })

            continue


        # ====================================================
        # GUARDRAIL
        # ====================================================

        guardrail = check_guardrail(

            transaction,

            action
        )


        # ====================================================
        # HUMAN APPROVAL REQUIRED
        #
        # IMPORTANT:
        # We check the guardrail itself instead of checking
        # only action == ESCALATE.
        #
        # This supports cases where REMIND/RETRY/etc. are
        # also blocked by merchant authority.
        # ====================================================

        approval_required = (

            isinstance(
                guardrail,
                dict
            )

            and

            guardrail.get(
                "approval_required"
            )
            is True
        )


        if approval_required:

            pending.append({

                "transaction":
                    transaction,

                "transaction_id":
                    transaction_id,

                "action":
                    action,

                "guardrail":
                    guardrail,

                "status":
                    "PENDING_APPROVAL"
            })

            continue


        # ====================================================
        # AUTONOMOUS EXECUTION
        # ====================================================

        execution = execute_payment_action(

            transaction,

            decision,

            guardrail
        )


        executed.append({

            "transaction_id":
                transaction_id,

            "action":
                action,

            "status":
                execution.get(
                    "status",
                    "EXECUTED"
                ),

            "executed":
                execution.get(
                    "executed",
                    True
                ),

            "message":
                execution.get(
                    "message",
                    "Recovery action executed."
                )
        })


    # ========================================================
    # RESULT
    # ========================================================

    return {

        "project":
            "RecoverAI",

        "status":
            "completed",

        "summary": {

            "total_transactions":
                len(transactions),

            "executed":
                len(executed),

            "pending_approval":
                len(pending),

            "rejected":
                len(rejected)
        },

        "executed":
            executed,

        "pending_approvals":
            pending,

        "rejected":
            rejected,

        "message":
            (
                "Recovery Agent completed: "
                f"{len(executed)} executed, "
                f"{len(pending)} pending approval, "
                f"{len(rejected)} rejected."
            )
    }


# ============================================================
# DASHBOARD
# ============================================================

@app.get("/dashboard")
def dashboard():

    df = load_transactions()

    transactions = df.to_dict(
        orient="records"
    )


    # ========================================================
    # REVENUE
    # ========================================================

    revenue = analyze_revenue(
        transactions
    )


    # ========================================================
    # RECOVERY DECISIONS
    # ========================================================

    recovery_decisions = []

    for transaction in transactions:

        decision = choose_recovery_action(
            transaction
        )

        recovery_decisions.append({

            "transaction":
                transaction,

            "decision":
                decision
        })


    # ========================================================
    # GUARDRAILS
    # ========================================================

    guardrail_results = []


    for item in recovery_decisions:

        transaction = item[
            "transaction"
        ]

        decision = item[
            "decision"
        ]


        transaction_id = get_transaction_id(
            transaction
        )

        action = decision.get(
            "action",
            "STOP"
        )


        saved_approval = get_approval(
            transaction_id
        )


        # ----------------------------------------------------
        # REJECTED
        # ----------------------------------------------------

        if (
            saved_approval
            and
            saved_approval.get("status")
            == "REJECTED"
        ):

            guardrail = {

                "allowed":
                    False,

                "approval_required":
                    False,

                "human_approved":
                    False,

                "status":
                    "REJECTED",

                "reason":
                    (
                        "Recovery action rejected "
                        "by human reviewer."
                    )
            }


        # ----------------------------------------------------
        # APPROVED
        # ----------------------------------------------------

        elif (
            saved_approval
            and
            saved_approval.get("status")
            == "EXECUTED"
        ):

            guardrail = {

                "allowed":
                    True,

                "approval_required":
                    False,

                "human_approved":
                    True,

                "status":
                    "APPROVED",

                "reason":
                    (
                        "Human approval already "
                        "received."
                    )
            }


        # ----------------------------------------------------
        # NEW TRANSACTION
        # ----------------------------------------------------

        else:

            guardrail = check_guardrail(

                transaction,

                action
            )


        guardrail_results.append({

            "transaction":
                transaction,

            "transaction_id":
                transaction_id,

            "action":
                action,

            "guardrail":
                guardrail
        })


    # ========================================================
    # CASH FLOW
    # ========================================================

    cashflow = analyze_cashflow(
        transactions
    )


    # ========================================================
    # PENDING APPROVALS
    # ========================================================

    pending_approvals = []


    for item in guardrail_results:

        transaction_id = item[
            "transaction_id"
        ]

        action = item[
            "action"
        ]

        guardrail = item[
            "guardrail"
        ]


        # Already processed

        saved_approval = get_approval(
            transaction_id
        )

        if saved_approval is not None:
            continue


        # Guardrail requires human

        if (
            isinstance(
                guardrail,
                dict
            )

            and

            guardrail.get(
                "approval_required"
            )
            is True
        ):

            pending_approvals.append(
                item
            )


    # ========================================================
    # SUMMARY
    # ========================================================

    revenue_at_risk = revenue.get(
        "revenue_at_risk",
        0
    )


    potentially_recoverable = revenue.get(
        "potentially_recoverable",
        0
    )


    # Fallback calculation

    if potentially_recoverable == 0:

        potentially_recoverable = sum(

            item[
                "transaction"
            ].get(
                "amount",
                0
            )

            for item in recovery_decisions

            if item[
                "decision"
            ].get(
                "action"
            )
            in [
                "RETRY",
                "REMIND"
            ]
        )


    cash_improvement = cashflow.get(

        "cash_position_improvement",

        0
    )


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "project":
            "RecoverAI",

        "status":
            "operational",

        "summary": {

            "total_transactions":
                len(transactions),

            "revenue_at_risk":
                revenue_at_risk,

            "potentially_recoverable":
                potentially_recoverable,

            "cash_position_improvement":
                cash_improvement,

            "pending_approvals":
                len(pending_approvals)
        },

        "revenue_intelligence":
            revenue,

        "recovery_strategy":
            recovery_decisions,

        "guardrails":
            guardrail_results,

        "cashflow":
            cashflow,

        "pending_approvals":
            pending_approvals,

        "approval_history":
            get_all_approvals()
    }