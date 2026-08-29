# RecoverAI 🚀

## AI-Powered Revenue Recovery & Cash-Flow Intelligence Platform

RecoverAI is an AI-powered revenue recovery agent designed to help merchants recover revenue lost through failed payments, abandoned checkouts, overdue invoices, and subscription payment failures.

Instead of simply detecting failed payments, RecoverAI analyzes transaction behavior, predicts recoverable revenue, selects the safest recovery action, applies guardrails, executes permitted actions, and estimates the impact on the merchant's future cash flow.

---

## 🎯 Problem

Small and medium-sized merchants can lose significant revenue because of:

* Failed payments
* Abandoned checkouts
* Overdue invoices
* Subscription payment failures
* Missed payment retries
* Manual recovery processes

Traditional payment systems identify payment failures but often leave merchants to decide what action to take.

RecoverAI turns this into an intelligent, automated recovery workflow.

---

## 💡 Solution

RecoverAI creates an intelligent revenue recovery loop:

```text
Transaction Data
       ↓
Revenue Intelligence
       ↓
Recovery Agent
       ↓
Guardrail Engine
       ↓
 ┌───────────────────────┬──────────────────────┐
 │ Autonomous Recovery   │ Human Approval       │
 │                       │                      │
 │ RETRY                 │ ESCALATE             │
 │ REMIND                │                      │
 │ STOP                  │                      │
 └───────────────────────┴──────────────────────┘
       ↓
Payment Execution
       ↓
Cash-Flow Forecast
       ↓
Merchant Dashboard
```

---

## ✨ Key Features

### 🤖 AI Revenue Intelligence

* Identifies transactions at risk of being lost
* Analyzes transaction behavior
* Estimates potentially recoverable revenue
* Prioritizes recovery opportunities

### 🔄 Recovery Agent

The Recovery Agent determines the safest action for each transaction:

* **RETRY** — attempt payment recovery
* **REMIND** — notify the customer about the pending payment
* **STOP** — stop recovery attempts when further action is not appropriate
* **ESCALATE** — send the transaction for human approval

### 🛡️ Guardrail Engine

RecoverAI does not blindly execute every AI recommendation.

The Guardrail Engine determines whether an action can be executed automatically or requires human authorization.

This creates a human-in-the-loop safety layer for higher-risk recovery actions.

### 👤 Human Approval Center

Transactions requiring authorization appear in the approval queue.

The merchant/evaluator can:

* Approve a recovery action
* Reject a recovery action
* Review the transaction and recommended action
* See the resulting execution status

This allows evaluators to verify that the recovery workflow is actually functioning.

### 💳 Payment Execution

Approved recovery actions are passed to the payment execution layer.

The project includes a Razorpay test integration layer for demonstrating payment recovery workflows in a test environment.

### 📊 Cash-Flow Intelligence

RecoverAI estimates how recovered transactions can affect the merchant's future cash position.

The dashboard provides:

* Current cash position
* Expected cash improvement
* Recovery impact
* Future cash-flow projections

### 📈 Merchant Dashboard

The dashboard provides a centralized view of:

* Revenue at risk
* Potentially recoverable revenue
* Cash-flow improvement
* Recovery actions
* Pending approvals
* Transaction status

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │   Merchant / Admin  │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │   React Dashboard   │
                    │       + Vite        │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │    FastAPI Backend  │
                    └──────────┬──────────┘
                               ↓
              ┌────────────────────────────────┐
              │       Revenue Intelligence     │
              └───────────────┬────────────────┘
                              ↓
              ┌────────────────────────────────┐
              │         Recovery Agent         │
              └───────────────┬────────────────┘
                              ↓
              ┌────────────────────────────────┐
              │        Guardrail Engine        │
              └───────────────┬────────────────┘
                              ↓
                  ┌───────────┴───────────┐
                  ↓                       ↓
        ┌──────────────────┐    ┌──────────────────┐
        │ Autonomous Action│    │ Human Approval   │
        │ RETRY / REMIND   │    │ APPROVE / REJECT │
        │ STOP             │    │ ESCALATE         │
        └────────┬─────────┘    └────────┬─────────┘
                 └────────────┬──────────┘
                              ↓
                    ┌─────────────────────┐
                    │  Payment Agent      │
                    │ Razorpay Test APIs  │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Cash-Flow Forecast  │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Merchant Dashboard  │
                    └─────────────────────┘
```

---

## 🧩 Technology Stack

### Frontend

* React
* Vite
* Axios
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* Uvicorn

### Data

* CSV transaction dataset
* SQLite approval database

### Payment Layer

* Razorpay test APIs / test integration layer

---

## 📁 Project Structure

```text
RecoverAI/
│
├── backend/
│   ├── agents/
│   │   ├── cashflow_agent.py
│   │   ├── payment_agent.py
│   │   ├── recovery_agent.py
│   │   └── revenue_agent.py
│   │
│   ├── services/
│   │   ├── forcast_service.py
│   │   ├── razorpay_service.py
│   │   └── recovery_service.py
│   │
│   ├── utils/
│   │   └── guardrails.py
│   │
│   ├── approval_database.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── requirements.txt
│
├── data/
│   └── transactions.csv
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── package.json
├── package-lock.json
├── .gitignore
└── README.md
```

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Tejasree46/RecoverAI.git
cd RecoverAI
```

### 2. Start the Backend

Open a terminal:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

---

## 🧪 Demo Workflow

1. Open the RecoverAI dashboard.
2. Review the revenue-at-risk metrics.
3. Run the Recovery Agent.
4. The agent analyzes the available transactions.
5. Recovery actions are selected.
6. Guardrails determine which actions can execute automatically.
7. Higher-risk actions appear in the Human Approval Center.
8. Approve or reject pending transactions.
9. Approved transactions proceed through the payment execution layer.
10. Rejected transactions remain blocked.
11. Dashboard metrics and recovery status update accordingly.
12. Review the projected cash-flow impact.

---

## 🔐 Human-in-the-Loop Design

RecoverAI is designed around controlled AI autonomy.

The AI can make recovery recommendations, but guardrails determine whether those recommendations can be executed automatically.

This prevents the recovery agent from taking unrestricted actions and provides a clear approval mechanism for higher-risk transactions.

```text
AI Recommendation
       ↓
Guardrail Check
       ↓
 ┌───────────────┐
 │ Safe to       │
 │ Execute?      │
 └───────┬───────┘
         ↓
    ┌────┴────┐
    ↓         ↓
   YES        NO
    ↓         ↓
 Execute   Human Approval
             ↓
        ┌────┴────┐
        ↓         ↓
     Approve    Reject
        ↓         ↓
     Execute     Block
```

---

## 🎯 Buildathon Focus

RecoverAI demonstrates how AI agents can be applied to payment and revenue operations while maintaining controlled execution.

The project combines:

* AI-driven revenue intelligence
* Automated recovery decisions
* Payment recovery workflows
* Human-in-the-loop approvals
* Guardrail-based execution
* Cash-flow forecasting
* Merchant-focused analytics

---

## 🏆 Vision

RecoverAI aims to move payment recovery from a reactive process into an intelligent revenue optimization system.

Instead of asking:

> "Which payments failed?"

RecoverAI asks:

> "Which revenue is at risk, what is the safest way to recover it, and how will recovery affect the merchant's future cash flow?"

---

## ⚠️ Demo / Test Environment

This project is intended as a buildathon demonstration.

Payment operations are demonstrated using a test/sandbox environment and should not be treated as production payment infrastructure without additional security, compliance, monitoring, authentication, and payment-provider validation.

---

## 👩‍💻 Project

**RecoverAI — AI Revenue Recovery & Cash-Flow Intelligence Platform**

Built for the Razorpay Buildathon.
