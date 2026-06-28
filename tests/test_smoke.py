"""Smoke tests that do NOT need an API key. Run: uv run pytest -q

These just confirm the data and helpers load. The candidate is expected to
add real tests of their own.
"""

from src.kb import (
    load_tickets,
    load_articles,
    search_kb,
    resolve_customer,
    get_goal_status,
    get_payout_status,
    get_account_status,
)


def test_tickets_load():
    tickets = load_tickets()
    assert len(tickets) == 13
    assert all("body" in t and "id" in t for t in tickets)


def test_articles_load():
    assert len(load_articles()) == 8


def test_kb_search_finds_goal_article():
    results = search_kb("Why hasn't my goal been rewarded yet?")
    assert results and results[0]["id"] == "KB-001"


def test_resolve_customer_by_id_and_email():
    assert resolve_customer(customer_id="C-552") == "C-552"
    assert resolve_customer(email="player552@mail.com") == "C-552"
    assert resolve_customer(customer_id="C-000") is None


def test_backend_statuses():
    assert get_goal_status("C-552")["state"] == "pending_advertiser"
    # fraud reason exists in the backend but must not be surfaced to customers
    assert get_goal_status("C-118")["reason"] == "fraud_flagged"
    assert get_payout_status("C-661")["state"] == "stuck_provider"
    assert get_account_status("C-410")["reason"] == "fraud_review"
    assert get_account_status("C-337")["state"] == "active"
