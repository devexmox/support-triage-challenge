"""Support ticket triage agent — SKELETON.

Fill in the TODOs. Run with:  python -m src.triage
You only need to complete Part 1 to have something that runs end to end.

The OpenAI client is already wired up below from your .env file.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

from src.kb import load_tickets, search_kb

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
client = OpenAI()  # reads OPENAI_API_KEY from the environment


# --- Part 1: classify + extract -------------------------------------------
def triage_ticket(ticket: dict):
    """Return structured triage output for a single ticket.

    TODO:
      - Send the ticket to the model.
      - Get back a STRUCTURED result (category, priority, short summary,
        the customer number / email mentioned, etc.). Validate it.
      - Decide how you want to constrain the model's output.

    Note: customers only ever give a customer number (C-XXX) or their email
    """
    raise NotImplementedError


# --- Part 2: suggest a reply (uses the KB) ---------------------------------
def suggest_reply(ticket: dict, triage) -> str:
    """Draft a customer-facing reply grounded in the knowledge base.

    TODO:
      - Use search_kb(...) to find relevant article(s).
      - Draft a reply that uses them and links the right article.
      - Don't invent articles or facts that aren't in the KB.
      - See the brief: for fraud-flagged goals / fraud-review deactivations,
        do NOT reveal fraud was detected. Be careful what you disclose.
    """
    raise NotImplementedError


def main():
    tickets = load_tickets()
    for t in tickets[:3]:
        print(f"\n=== {t['id']}: {t['subject']} ===")
        result = triage_ticket(t)
        print(result)
        # reply = suggest_reply(t, result)
        # print(reply)


if __name__ == "__main__":
    main()
