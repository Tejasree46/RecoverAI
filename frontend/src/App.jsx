import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";


function App() {

  const [dashboard, setDashboard] = useState(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  const [processing, setProcessing] = useState(null);

  const [message, setMessage] = useState("");

  const [activePage, setActivePage] =
    useState("dashboard");


  // ==========================================================
  // LOAD DASHBOARD
  // ==========================================================

  useEffect(() => {

    loadDashboard();

  }, []);


  async function loadDashboard() {

    try {

      setLoading(true);

      setError("");

      const response = await axios.get(
        `${API_URL}/dashboard`
      );

      setDashboard(
        response.data
      );

    } catch (err) {

      console.error(
        "RecoverAI dashboard error:",
        err
      );

      if (err.response) {

        setError(
          `Backend error: ${err.response.status}`
        );

      } else {

        setError(
          "Unable to connect to RecoverAI backend."
        );
      }

    } finally {

      setLoading(false);
    }
  }


  // ==========================================================
  // RUN RECOVERY AGENT
  // ==========================================================

  async function runRecoveryAgent() {

    try {

      setMessage(
        "Running Recovery Agent..."
      );

      const response = await axios.get(
        `${API_URL}/execute-recovery`
      );

      console.log(
        "Recovery Agent:",
        response.data
      );


      const result =
        response.data;


      const summary =
        result.summary || {};


      setMessage(

        `Recovery Agent completed: ` +

        `${summary.executed || 0} executed, ` +

        `${summary.pending_approval || 0} pending approval, ` +

        `${summary.rejected || 0} rejected.`
      );


      await loadDashboard();


      // Automatically show approvals
      // if new approvals exist.

      if (
        Number(
          summary.pending_approval || 0
        ) > 0
      ) {

        setActivePage(
          "approvals"
        );
      }

    } catch (err) {

      console.error(
        "Recovery Agent error:",
        err.response?.data || err
      );


      setMessage(

        `Recovery Agent failed: ${
          err.response?.data?.detail ||
          err.response?.status ||
          "backend error"
        }`
      );
    }
  }


  // ==========================================================
  // HUMAN APPROVAL
  // ==========================================================

  async function handleApproval(
    transactionId,
    approved
  ) {

    try {

      setProcessing(
        transactionId
      );

      setMessage(
        `${approved ? "Approving" : "Rejecting"} ${transactionId}...`
      );


      const response =
        await axios.post(

          `${API_URL}/approval`,

          {
            transaction_id:
              transactionId,

            approved:
              approved
          },

          {
            headers: {
              "Content-Type":
                "application/json",

              Accept:
                "application/json"
            }
          }
        );


      console.log(
        "Approval response:",
        response.data
      );


      setMessage(

        approved

          ? `${transactionId}: Approved successfully. Recovery action authorized.`

          : `${transactionId}: Rejected successfully. Recovery action blocked.`
      );


      await loadDashboard();


    } catch (err) {

      console.error(
        "Approval error:",
        err.response?.data || err
      );


      setMessage(

        `Unable to process ${transactionId}: ${
          err.response?.data?.detail ||
          err.response?.statusText ||
          "Approval failed"
        }`
      );

    } finally {

      setProcessing(null);
    }
  }


  // ==========================================================
  // HELPERS
  // ==========================================================

  function formatCurrency(value) {

    const number =
      Number(value);


    if (
      !Number.isFinite(number)
    ) {

      return "₹0";
    }


    return `₹${number.toLocaleString(
      "en-IN",
      {
        maximumFractionDigits: 0
      }
    )}`;
  }


  function getTransactionId(
    item,
    index
  ) {

    return (

      item?.transaction_id ||

      item?.transaction?.transaction_id ||

      item?.transaction?.id ||

      item?.id ||

      `TXN${String(
        index + 1
      ).padStart(3, "0")}`
    );
  }


  function getAction(item) {

    return (

      item?.decision?.action ||

      item?.action ||

      item?.recommended_action ||

      "STOP"
    );
  }


  function getGuardrail(
    item
  ) {

    const guardrail =
      item?.guardrail;


    if (!guardrail) {

      return "Checked";
    }


    if (
      guardrail.status ===
      "REJECTED"
    ) {

      return "Rejected";
    }


    if (
      guardrail.status ===
      "APPROVED"
    ) {

      return "Approved";
    }


    if (
      guardrail.approval_required
    ) {

      return "Approval Required";
    }


    return "Checked";
  }


  function getStatus(
    item,
    action
  ) {

    if (item?.status) {

      return item.status;
    }


    const guardrail =
      item?.guardrail;


    if (
      guardrail?.status ===
      "REJECTED"
    ) {

      return "Rejected";
    }


    if (
      guardrail?.status ===
      "APPROVED"
    ) {

      return "Approved";
    }


    if (
      guardrail?.approval_required
    ) {

      return "Pending";
    }


    if (
      action === "STOP"
    ) {

      return "Stopped";
    }


    return "Ready";
  }


  // ==========================================================
  // LOADING
  // ==========================================================

  if (loading) {

    return (

      <div className="loading-screen">

        <div className="loading-logo">
          R
        </div>

        <h2>
          RecoverAI
        </h2>

        <p>
          Loading Revenue Command Center...
        </p>

      </div>
    );
  }


  // ==========================================================
  // ERROR
  // ==========================================================

  if (error) {

    return (

      <div className="error-screen">

        <div className="error-box">

          <div className="brand-mark">
            R
          </div>

          <h1>
            RecoverAI
          </h1>

          <p>
            {error}
          </p>

          <button
            className="primary-button"
            onClick={loadDashboard}
          >
            ↻ Retry
          </button>

        </div>

      </div>
    );
  }


  // ==========================================================
  // DATA
  // ==========================================================

  const summary =
    dashboard?.summary || {};


  const recovery =
    dashboard?.recovery_strategy || [];


  const pendingApprovals =
    dashboard?.pending_approvals || [];


  const cashflow =
    dashboard?.cashflow || {};


  const forecast =
    cashflow?.forecast ||
    dashboard?.forecast ||
    [];


  const approvalHistory =
    dashboard?.approval_history ||
    [];


  // ==========================================================
  // SIDEBAR
  // ==========================================================

  function Sidebar() {

    return (

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-mark">
            R
          </div>

          <div>

            <h1>
              RecoverAI
            </h1>

            <span>
              CONTROL CENTER
            </span>

          </div>

        </div>


        <div className="environment">

          <span className="online-dot" />

          <span>
            TEST ENVIRONMENT
          </span>

        </div>


        <nav className="sidebar-nav">

          <button
            className={
              activePage === "dashboard"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              setActivePage("dashboard")
            }
          >
            <span>⌂</span>
            Dashboard
          </button>


          <button
            className={
              activePage === "recovery"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              setActivePage("recovery")
            }
          >
            <span>↻</span>
            Recovery Actions
          </button>


          <button
            className={
              activePage === "cashflow"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              setActivePage("cashflow")
            }
          >
            <span>⌁</span>
            Cash Flow
          </button>


          <button
            className={
              activePage === "approvals"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              setActivePage("approvals")
            }
          >
            <span>✓</span>
            Approvals

            {pendingApprovals.length > 0 && (

              <span className="nav-count">

                {pendingApprovals.length}

              </span>

            )}

          </button>

        </nav>


        <div className="sidebar-bottom">

          <div className="system-status">

            <span className="online-dot" />

            <div>

              <strong>
                System Operational
              </strong>

              <small>
                All recovery services online
              </small>

            </div>

          </div>


          <div className="sidebar-footer">

            <strong>
              RecoverAI
            </strong>

            <span>
              AI Revenue Recovery Platform
            </span>

          </div>

        </div>

      </aside>
    );
  }


  // ==========================================================
  // HEADER
  // ==========================================================

  function Header({
    eyebrow,
    title,
    subtitle
  }) {

    return (

      <header className="page-header">

        <div>

          <div className="eyebrow">
            {eyebrow}
          </div>

          <h1>
            {title}
          </h1>

          <p>
            {subtitle}
          </p>

        </div>


        <div className="header-actions">

          <div className="test-pill">

            <span className="online-dot" />

            TEST ENVIRONMENT

          </div>


          <button
            className="secondary-button"
            onClick={loadDashboard}
          >
            ↻ Refresh
          </button>


          <button
            className="primary-button"
            onClick={runRecoveryAgent}
          >
            ▶ Run Recovery Agent
          </button>

        </div>

      </header>
    );
  }


  // ==========================================================
  // MESSAGE
  // ==========================================================

  function Message() {

    if (!message) {

      return null;
    }


    const isError =
      message.includes(
        "failed"
      ) ||
      message.includes(
        "Unable"
      );


    return (

      <div
        className={
          isError
            ? "alert error-alert"
            : "alert success-alert"
        }
      >

        <span>
          {isError ? "!" : "✓"}
        </span>

        {message}

      </div>
    );
  }


  // ==========================================================
  // DASHBOARD
  // ==========================================================

  function DashboardPage() {

    return (

      <>

        <Header
          eyebrow="REVENUE COMMAND CENTER"
          title="Autonomous Recovery"
          subtitle="AI-powered revenue recovery, guardrails and cash-flow intelligence."
        />


        <Message />


        <section className="kpi-grid">

          <div className="kpi-card risk">

            <div className="kpi-top">

              <span>
                REVENUE AT RISK
              </span>

              <b>!</b>

            </div>

            <strong>
              {formatCurrency(
                summary.revenue_at_risk
              )}
            </strong>

            <small>
              Revenue currently at risk
            </small>

            <div className="progress">
              <div />
            </div>

          </div>


          <div className="kpi-card recoverable">

            <div className="kpi-top">

              <span>
                POTENTIALLY RECOVERABLE
              </span>

              <b>↗</b>

            </div>

            <strong>
              {formatCurrency(
                summary.potentially_recoverable
              )}
            </strong>

            <small>
              Expected recoverable revenue
            </small>

            <div className="progress">
              <div />
            </div>

          </div>


          <div className="kpi-card improvement">

            <div className="kpi-top">

              <span>
                CASH IMPROVEMENT
              </span>

              <b>₹</b>

            </div>

            <strong>
              {formatCurrency(
                summary.cash_position_improvement
              )}
            </strong>

            <small>
              Expected 7-day improvement
            </small>

            <div className="progress">
              <div />
            </div>

          </div>


          <div className="kpi-card approval">

            <div className="kpi-top">

              <span>
                HUMAN APPROVAL
              </span>

              <b>✓</b>

            </div>

            <strong>
              {summary.pending_approvals ?? 0}
            </strong>

            <small>
              Transactions awaiting review
            </small>

            <div className="progress">
              <div />
            </div>

          </div>

        </section>


        <section className="two-column">

          <div className="panel strategy-panel">

            <div className="panel-heading">

              <div>

                <div className="eyebrow">
                  AI STRATEGY
                </div>

                <h2>
                  Recovery Strategy
                </h2>

                <p>
                  RecoverAI evaluates every at-risk transaction before selecting the safest action.
                </p>

              </div>

              <div className="purple-icon">
                ✦
              </div>

            </div>


            <div className="strategy-grid">

              <div>
                <strong>
                  {
                    recovery.filter(
                      x =>
                        getAction(x) ===
                        "RETRY"
                    ).length
                  }
                </strong>

                <span>
                  Retry
                </span>
              </div>


              <div>
                <strong>
                  {
                    recovery.filter(
                      x =>
                        getAction(x) ===
                        "REMIND"
                    ).length
                  }
                </strong>

                <span>
                  Reminder
                </span>
              </div>


              <div>
                <strong>
                  {
                    recovery.filter(
                      x =>
                        getAction(x) ===
                        "INCENTIVE"
                    ).length
                  }
                </strong>

                <span>
                  Incentive
                </span>
              </div>


              <div>
                <strong>
                  {pendingApprovals.length}
                </strong>

                <span>
                  Human Review
                </span>
              </div>

            </div>


            <div className="strategy-note">

              ✦

              <div>

                <strong>
                  Autonomous recovery with guardrails
                </strong>

                <span>
                  Transactions exceeding merchant authority are automatically routed to human approval.
                </span>

              </div>

            </div>

          </div>


          <div className="panel performance-panel">

            <div className="eyebrow">
              RECOVERY INTELLIGENCE
            </div>

            <h2>
              Agent Performance
            </h2>


            <div className="score-ring">

              <div>

                <strong>
                  95%
                </strong>

                <span>
                  Recovery confidence
                </span>

              </div>

            </div>


            <div className="performance-stats">

              <div>
                <strong>
                  {recovery.length}
                </strong>

                <span>
                  analyzed
                </span>
              </div>

              <div>
                <strong>
                  {pendingApprovals.length}
                </strong>

                <span>
                  review
                </span>
              </div>

              <div>
                <strong>
                  {
                    recovery.filter(
                      x =>
                        x.guardrail?.status ===
                        "REJECTED"
                    ).length
                  }
                </strong>

                <span>
                  guardrail layer
                </span>
              </div>

            </div>

          </div>

        </section>


        <RecoveryTable
          limit={8}
        />

      </>

    );
  }


  // ==========================================================
  // RECOVERY TABLE
  // ==========================================================

  function RecoveryTable({
    limit
  }) {

    const rows =
      limit
        ? recovery.slice(0, limit)
        : recovery;


    return (

      <section className="panel">

        <div className="panel-heading">

          <div>

            <div className="eyebrow">
              AI DECISIONS
            </div>

            <h2>
              Recovery Actions
            </h2>

            <p>
              AI-selected actions and guardrail decisions for at-risk transactions.
            </p>

          </div>

          {limit && (

            <button
              className="text-button"
              onClick={() =>
                setActivePage(
                  "recovery"
                )
              }
            >
              View all →
            </button>

          )}

        </div>


        <div className="table-wrap">

          <table>

            <thead>

              <tr>

                <th>
                  TRANSACTION
                </th>

                <th>
                  ACTION
                </th>

                <th>
                  GUARDRAIL
                </th>

                <th>
                  AMOUNT
                </th>

                <th>
                  STATUS
                </th>

              </tr>

            </thead>


            <tbody>

              {rows.length === 0 ? (

                <tr>

                  <td
                    colSpan="5"
                    className="empty-cell"
                  >
                    No recovery actions available.
                  </td>

                </tr>

              ) : (

                rows.map(
                  (item, index) => {

                    const transaction =
                      item?.transaction ||
                      {};

                    const transactionId =
                      getTransactionId(
                        item,
                        index
                      );

                    const action =
                      getAction(item);

                    const status =
                      getStatus(
                        item,
                        action
                      );

                    return (

                      <tr
                        key={
                          transactionId
                        }
                      >

                        <td>
                          <strong>
                            {transactionId}
                          </strong>
                        </td>


                        <td>

                          <span
                            className={`action-badge action-${action.toLowerCase()}`}
                          >
                            {action}
                          </span>

                        </td>


                        <td>

                          <span className="guardrail-text">

                            {getGuardrail(
                              item
                            )}

                          </span>

                        </td>


                        <td>

                          {formatCurrency(
                            transaction.amount
                          )}

                        </td>


                        <td>

                          <span
                            className={`status-badge status-${status
                              .toLowerCase()
                              .replaceAll(
                                " ",
                                "-"
                              )}`}
                          >
                            {status}
                          </span>

                        </td>

                      </tr>

                    );
                  }
                )

              )}

            </tbody>

          </table>

        </div>

      </section>

    );
  }


  // ==========================================================
  // CASH FLOW PAGE
  // ==========================================================

  function CashFlowPage() {

    const maxCash =
      Math.max(

        Number(
          cashflow.projected_cash_7_days
        ) || 1,

        ...forecast.map(
          day =>
            Number(
              day.projected_cash ??
              day.cash ??
              0
            )
        )
      );


    return (

      <>

        <Header
          eyebrow="CASH-FLOW INTELLIGENCE"
          title="7-Day Cash Flow Forecast"
          subtitle="Projected cash position after RecoverAI recovery decisions."
        />


        <Message />


        <section className="panel cash-panel">

          <div className="panel-heading">

            <div>

              <div className="eyebrow">
                FORECAST
              </div>

              <h2>
                Expected Cash Position
              </h2>

              <p>
                Expected impact of revenue recovery over the next seven days.
              </p>

            </div>

          </div>


          <div className="forecast">

            {forecast.length === 0 ? (

              <div className="empty-cell">
                No forecast data available.
              </div>

            ) : (

              forecast.map(
                (day, index) => {

                  const value =
                    Number(
                      day.projected_cash ??
                      day.cash ??
                      0
                    );


                  const height =
                    Math.max(
                      10,
                      (
                        value /
                        maxCash
                      ) *
                      100
                    );


                  return (

                    <div
                      className="forecast-day"
                      key={index}
                    >

                      <div className="bar-area">

                        <div
                          className="bar"
                          style={{
                            height:
                              `${height}%`
                          }}
                        />

                      </div>

                      <span>
                        Day{" "}
                        {day.day ??
                          index + 1}
                      </span>

                      <strong>
                        {formatCurrency(
                          value
                        )}
                      </strong>

                    </div>

                  );
                }
              )

            )}

          </div>


          <div className="cash-summary">

            <div>

              <span>
                Current Cash
              </span>

              <strong>
                {formatCurrency(
                  cashflow.current_cash
                )}
              </strong>

            </div>


            <div>

              <span>
                7-Day Projection
              </span>

              <strong>
                {formatCurrency(
                  cashflow.projected_cash_7_days
                )}
              </strong>

            </div>


            <div>

              <span>
                Expected Improvement
              </span>

              <strong className="positive">
                {formatCurrency(
                  cashflow.cash_position_improvement
                )}
              </strong>

            </div>

          </div>

        </section>

      </>

    );
  }


  // ==========================================================
  // APPROVALS PAGE
  // ==========================================================

  function ApprovalsPage() {

    return (

      <>

        <Header
          eyebrow="HUMAN-IN-THE-LOOP"
          title="Human Approval Center"
          subtitle="Review recovery actions that exceed autonomous authority."
        />


        <Message />


        <section className="approval-hero">

          <div>

            <div className="eyebrow">
              HUMAN-IN-THE-LOOP
            </div>

            <h2>
              {pendingApprovals.length}
              {" "}
              pending approvals
            </h2>

            <p>
              Transactions blocked by RecoverAI guardrails require explicit human authorization.
            </p>

          </div>


          <div className="hero-check">
            ✓
          </div>

        </section>


        <section className="panel">

          <div className="panel-heading">

            <div>

              <div className="eyebrow">
                GUARDRAIL REVIEW
              </div>

              <h2>
                Review Transactions
              </h2>

              <p>
                Approve or reject each blocked recovery action.
              </p>

            </div>


            <span className="guardrail-pill">
              GUARDRAILS ACTIVE
            </span>

          </div>


          {pendingApprovals.length === 0 ? (

            <div className="no-pending">

              <strong>
                ✓ No pending approvals
              </strong>

              <span>
                All recovery decisions are currently authorized or completed.
              </span>

            </div>

          ) : (

            <div className="approval-list">

              {pendingApprovals.map(
                (item, index) => {

                  const transaction =
                    item?.transaction ||
                    {};

                  const transactionId =
                    getTransactionId(
                      item,
                      index
                    );

                  const action =
                    getAction(item);

                  const amount =
                    transaction.amount;

                  const isProcessing =
                    processing ===
                    transactionId;


                  return (

                    <div
                      className="approval-row"
                      key={
                        transactionId
                      }
                    >

                      <div className="approval-icon">
                        !
                      </div>


                      <div className="approval-main">

                        <strong>
                          {transactionId}
                        </strong>

                        <span>
                          {action}
                          {" • "}
                          {formatCurrency(
                            amount
                          )}
                        </span>

                      </div>


                      <div className="approval-reason">

                        <span>
                          GUARDRAIL
                        </span>

                        <strong>
                          Human authorization required
                        </strong>

                      </div>


                      <div className="approval-buttons">

                        <button
                          className="approve-button"
                          disabled={
                            isProcessing
                          }
                          onClick={() =>
                            handleApproval(
                              transactionId,
                              true
                            )
                          }
                        >

                          {isProcessing
                            ? "Processing..."
                            : "✓ Approve"}

                        </button>


                        <button
                          className="reject-button"
                          disabled={
                            isProcessing
                          }
                          onClick={() =>
                            handleApproval(
                              transactionId,
                              false
                            )
                          }
                        >

                          {isProcessing
                            ? "Processing..."
                            : "Reject"}

                        </button>

                      </div>

                    </div>

                  );

                }
              )}

            </div>

          )}

        </section>


        <section className="panel">

          <div className="panel-heading">

            <div>

              <div className="eyebrow">
                CONTROL FLOW
              </div>

              <h2>
                How Human Authorization Works
              </h2>

              <p>
                RecoverAI demonstrates bounded autonomy instead of unrestricted AI execution.
              </p>

            </div>

          </div>


          <div className="flow-grid">

            <div className="flow-card">

              <span>
                01
              </span>

              <strong>
                AI Decision
              </strong>

              <p>
                Recovery Agent selects the safest action based on transaction behavior.
              </p>

            </div>


            <div className="flow-card">

              <span>
                02
              </span>

              <strong>
                Guardrail Check
              </strong>

              <p>
                RecoverAI checks transaction amount and merchant authority.
              </p>

            </div>


            <div className="flow-card">

              <span>
                03
              </span>

              <strong>
                Human Approval
              </strong>

              <p>
                The evaluator can explicitly approve or reject the action.
              </p>

            </div>


            <div className="flow-card">

              <span>
                04
              </span>

              <strong>
                Execution
              </strong>

              <p>
                Approved actions proceed through the test payment environment.
              </p>

            </div>

          </div>

        </section>


        {approvalHistory.length > 0 && (

          <section className="panel">

            <div className="panel-heading">

              <div>

                <div className="eyebrow">
                  AUDIT TRAIL
                </div>

                <h2>
                  Human Decisions
                </h2>

                <p>
                  Previously approved and rejected recovery actions.
                </p>

              </div>

            </div>


            <div className="history-list">

              {approvalHistory.map(
                (item, index) => (

                  <div
                    className="history-row"
                    key={
                      item.transaction_id ||
                      index
                    }
                  >

                    <strong>
                      {
                        item.transaction_id
                      }
                    </strong>

                    <span>
                      {item.action}
                    </span>

                    <span
                      className={
                        item.status ===
                        "REJECTED"
                          ? "history-rejected"
                          : "history-approved"
                      }
                    >
                      {item.status}
                    </span>

                  </div>

                )
              )}

            </div>

          </section>

        )}

      </>

    );
  }


  // ==========================================================
  // RECOVERY PAGE
  // ==========================================================

  function RecoveryPage() {

    return (

      <>

        <Header
          eyebrow="AI DECISIONS"
          title="Recovery Actions"
          subtitle="Review how RecoverAI evaluates and routes every at-risk transaction."
        />


        <Message />


        <RecoveryTable />


        <section className="panel">

          <div className="panel-heading">

            <div>

              <div className="eyebrow">
                AGENT EXECUTION
              </div>

              <h2>
                Recovery Agent Execution
              </h2>

              <p>
                Latest recovery decisions and execution state.
              </p>

            </div>

            <button
              className="primary-button"
              onClick={runRecoveryAgent}
            >
              ▶ Run Agent
            </button>

          </div>


          <div className="execution-list">

            {recovery.map(
              (item, index) => {

                const transaction =
                  item?.transaction ||
                  {};

                const transactionId =
                  getTransactionId(
                    item,
                    index
                  );

                const action =
                  getAction(item);

                const status =
                  getStatus(
                    item,
                    action
                  );


                return (

                  <div
                    className="execution-row"
                    key={
                      transactionId
                    }
                  >

                    <span className="execution-dot" />

                    <div>

                      <strong>
                        {transactionId}
                      </strong>

                      <span>
                        {action}
                      </span>

                    </div>


                    <span
                      className={`status-badge status-${status
                        .toLowerCase()
                        .replaceAll(
                          " ",
                          "-"
                        )}`}
                    >
                      {status}
                    </span>


                    <strong>
                      {formatCurrency(
                        transaction.amount
                      )}
                    </strong>

                  </div>

                );

              }
            )}

          </div>

        </section>

      </>

    );
  }


  // ==========================================================
  // PAGE
  // ==========================================================

  function renderPage() {

    if (
      activePage ===
      "recovery"
    ) {

      return (
        <RecoveryPage />
      );
    }


    if (
      activePage ===
      "cashflow"
    ) {

      return (
        <CashFlowPage />
      );
    }


    if (
      activePage ===
      "approvals"
    ) {

      return (
        <ApprovalsPage />
      );
    }


    return (
      <DashboardPage />
    );
  }


  // ==========================================================
  // APP
  // ==========================================================

  return (

    <div className="app-shell">

      <Sidebar />


      <main className="main-content">

        {renderPage()}

      </main>

    </div>
  );
}


export default App;