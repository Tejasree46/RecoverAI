import sqlite3
from pathlib import Path


# ============================================================
# DATABASE LOCATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "approvals.db"


# ============================================================
# CREATE DATABASE
# ============================================================

def initialize_approval_database():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS approvals (

            transaction_id TEXT PRIMARY KEY,

            approved INTEGER NOT NULL,

            status TEXT NOT NULL,

            action TEXT,

            message TEXT

        )
        """
    )

    connection.commit()
    connection.close()


# ============================================================
# SAVE APPROVAL
# ============================================================

def save_approval(
    transaction_id,
    approved,
    status,
    action,
    message
):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO approvals
        (
            transaction_id,
            approved,
            status,
            action,
            message
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            transaction_id,
            1 if approved else 0,
            status,
            action,
            message
        )
    )

    connection.commit()
    connection.close()


# ============================================================
# GET APPROVAL
# ============================================================

def get_approval(transaction_id):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            transaction_id,
            approved,
            status,
            action,
            message

        FROM approvals

        WHERE transaction_id = ?
        """,
        (transaction_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "transaction_id": row[0],
        "approved": bool(row[1]),
        "status": row[2],
        "action": row[3],
        "message": row[4]
    }


# ============================================================
# GET ALL APPROVALS
# ============================================================

def get_all_approvals():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            transaction_id,
            approved,
            status,
            action,
            message

        FROM approvals
        """
    )

    rows = cursor.fetchall()

    connection.close()

    approvals = {}

    for row in rows:

        approvals[row[0]] = {
            "transaction_id": row[0],
            "approved": bool(row[1]),
            "status": row[2],
            "action": row[3],
            "message": row[4]
        }

    return approvals