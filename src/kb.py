"""Knowledge base access + a couple of mock backend tools.

This file is PROVIDED so you don't waste time building data plumbing. You can
use it as-is, wrap it, or ignore it. The KB search here is a naive keyword
matcher on purpose — improving or replacing retrieval is a fair extension.

NOTE on identifiers: customers can only give us their customer number
(format C-XXX) or the email on their account.
The mock backends below are keyed by customer.
"""

import json
import pathlib
from typing import Optional

_DATA = pathlib.Path(__file__).resolve().parent.parent / "data"


def load_json(name: str):
    with open(_DATA / name, "r", encoding="utf-8") as f:
        return json.load(f)


def load_tickets() -> list[dict]:
    return load_json("tickets.json")


def load_articles() -> list[dict]:
    return load_json("kb_articles.json")


def search_kb(query: str, top_k: int = 3) -> list[dict]:
    """Naive keyword overlap search over the KB. Returns up to top_k articles.

    Each result is the article dict plus a 'score' field. Feel free to replace
    this with embeddings or anything else.
    """
    articles = load_articles()
    q_tokens = {t for t in _tokenize(query) if len(t) > 2}
    scored = []
    for a in articles:
        haystack = " ".join([a["title"], a["body"], " ".join(a.get("tags", []))])
        a_tokens = set(_tokenize(haystack))
        score = len(q_tokens & a_tokens)
        if score:
            scored.append({**a, "score": score})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def _tokenize(text: str) -> list[str]:
    return "".join(c.lower() if c.isalnum() else " " for c in text).split()


# ----- Mock backend (for the tool-calling extension) -----------------------
#
# Pretend internal systems, keyed by customer number. A real agent would call
# these to find out what's actually going on with a customer's goal, payout,
# or account before replying.
#
# IMPORTANT (read the brief): some statuses are fraud-related. When a goal is
# rejected for fraud or an account is deactivated for fraud review, support
# policy is NOT to reveal that fraud was detected or explain the signals. Your
# agent has to decide how to use this information without leaking it.

_CUSTOMERS = {
    "C-552": {
        "email": "player552@mail.com",
        "account": "active",
        "goal": {"state": "pending_advertiser", "days_open": 3},
        "payout": None,
    },
    "C-118": {
        "email": "user118@mail.com",
        "account": "active",
        "goal": {"state": "rejected", "reason": "fraud_flagged"},
        "payout": None,
    },
    "C-274": {
        "email": "spieler274@mail.de",
        "account": "active",
        "goal": {"state": "rejected", "reason": "requirements_not_met"},
        "payout": None,
    },
    "C-661": {
        "email": "c661@mail.com",
        "account": "active",
        "goal": None,
        "payout": {"state": "stuck_provider", "provider": "PayPal", "days_open": 4},
    },
    "C-789": {
        "email": "c789@mail.com",
        "account": "active",
        "goal": None,
        "payout": {"state": "paid", "days_open": 1},
    },
    "C-205": {
        "email": "c205@mail.com",
        "account": "active",
        "goal": None,
        "payout": {
            "state": "stuck_provider",
            "provider": "bank transfer",
            "days_open": 6,
        },
    },
    "C-410": {
        "email": "c410@mail.com",
        "account": "deactivated",
        "account_reason": "fraud_review",
        "goal": None,
        "payout": None,
    },
    "C-846": {
        "email": "c846@mail.de",
        "account": "deactivated",
        "account_reason": "fraud_review",
        "goal": None,
        "payout": None,
    },
    "C-337": {
        "email": "c337@mail.fr",
        "account": "active",
        "goal": None,
        "payout": None,
    },
    "C-512": {
        "email": "c512@mail.com",
        "account": "active",
        "goal": None,
        "payout": {"state": "paid", "days_open": 1},
    },
    "C-159": {
        "email": "c159@mail.com",
        "account": "active",
        "goal": None,
        "payout": None,
    },
    "C-901": {
        "email": "c901@mail.de",
        "account": "active",
        "goal": None,
        "payout": None,
    },
    "C-633": {
        "email": "c633@mail.com",
        "account": "active",
        "goal": {"state": "rejected", "reason": "fraud_flagged"},
        "payout": None,
    },
}

_EMAIL_INDEX = {v["email"].lower(): cid for cid, v in _CUSTOMERS.items()}


def resolve_customer(
    *, customer_id: Optional[str] = None, email: Optional[str] = None
) -> Optional[str]:
    """Resolve a customer number from an id or email. Returns the id or None."""
    if customer_id and customer_id.strip().upper() in _CUSTOMERS:
        return customer_id.strip().upper()
    if email and email.strip().lower() in _EMAIL_INDEX:
        return _EMAIL_INDEX[email.strip().lower()]
    return None


def get_goal_status(customer_id: str) -> dict:
    """Latest goal status for a customer. {'state': 'not_found'} if unknown."""
    cust = _CUSTOMERS.get(customer_id.strip().upper())
    if not cust:
        return {"state": "customer_not_found"}
    return cust.get("goal") or {"state": "no_recent_goal"}


def get_payout_status(customer_id: str) -> dict:
    """Latest payout status for a customer."""
    cust = _CUSTOMERS.get(customer_id.strip().upper())
    if not cust:
        return {"state": "customer_not_found"}
    return cust.get("payout") or {"state": "no_recent_payout"}


def get_account_status(customer_id: str) -> dict:
    """Account status for a customer, including deactivation reason if any."""
    cust = _CUSTOMERS.get(customer_id.strip().upper())
    if not cust:
        return {"state": "customer_not_found"}
    out = {"state": cust["account"]}
    if "account_reason" in cust:
        out["reason"] = cust["account_reason"]
    return out
