# Live Coding Exercise — Support Ticket Triage Agent

**Format:** ~90 min coding (shared screen, we'll be watching and chatting) + ~20 min discussion.
**Language:** Python. **Model:** OpenAI (key provided). Any libraries welcome.

## The scenario

We run a mobile rewards app: users complete **goals** (offers) to earn rewards, then **request payouts**. Our support team gets a steady stream of tickets, and the large majority are one of three kinds:

1. **Goal not rewarded** — "I completed the goal but didn't get my reward." Sometimes it's still pending the advertiser; sometimes the steps weren't met; and sometimes **the user was flagged for fraud**.
2. **Payout is slow** — "I requested a payout and it hasn't arrived." Often it's simply **stuck with the third-party payment provider** (PayPal / bank).
3. **Account deactivated** — "My account was deactivated and I'm not a fraudster." These are appeals.

We want an **agent that triages each ticket and drafts a first-response** for a human agent to review and send.

You've been given a small scaffold (`README.md` explains the layout): sample tickets in `data/tickets.json`, help-center articles in `data/kb_articles.json`, and helpers in `src/kb.py`. These mock files stand in for our real tickets and Zendesk articles.

**Important about identifiers:** customers can only ever give us their **customer number** (format `C-XXX`) or the **email** on their account. There are no order/transaction numbers. The provided mock backend (`src/kb.py`) is keyed by customer.

We don't expect you to finish everything. **Get Part 1 working end-to-end first**, then go as far as you can. Talk us through your thinking as you go.

## Part 1 — Classify & extract _(core — aim to complete this)_

For each ticket, produce a **structured, validated** result with at least:

- **category** — from a small fixed set you define (goal tracking, payout, account deactivation, account access, …)
- **priority** — e.g. low / medium / high / urgent
- **summary** — one line a human agent can skim
- **identifiers** — the customer number and/or email mentioned in the ticket

It should run over all tickets and not crash on messy input. Think about how you constrain and validate the model's output.

## Part 2 — Draft a grounded reply _(strongly encouraged)_

For each ticket, draft a customer-facing reply **grounded in the knowledge base** (`search_kb` is provided). Reference/link the relevant article; do not invent articles, policies, or timeframes. Some tickets have no relevant article — handle that.

## Part 3 — Extensions _(pick what interests you; senior candidates: get into at least one)_

Not ordered by priority — choose what you'd defend as most valuable:

- **Fraud confidentiality (the interesting one).** The mock backend can report that a goal was rejected for fraud, or an account was deactivated for fraud review. **When that's the case, the reply must NOT reveal that fraud was detected or hint at the detection signals** — otherwise fraudsters learn how we catch them. The agent should still **write a careful, non-committal "under review" draft** (a human reviews and sends it) _and_ flag the ticket for human review — not skip the draft. How do you design this so the sensitive reason never leaks into the customer-facing text?
- **Tool calling.** `src/kb.py` exposes `resolve_customer`, `get_goal_status`, `get_payout_status`, `get_account_status` (all by customer number/email). Let the agent look the customer up and use their real status in the reply (e.g. "your payout is with the provider").
- **Confidence & escalation.** Add a confidence signal and route low-confidence or sensitive tickets (deactivation appeals, fraud cases, very angry customers) to a human. What's your policy and why?
- **Evaluation.** `data/labeled_eval.json` has ground-truth labels (including a `sensitive` flag). Build a small harness that measures classification accuracy, escalation, and whether you correctly caught the fraud-sensitive cases.
- **Robustness.** Retries/backoff, malformed output handling, cost/latency, batching.

## Discussion — learning from human review (talk-through, no code needed)

Human agents review and edit the drafts before sending. We'd like the system to
get better over time from that review signal. Be ready to discuss:

- What would you log from each review (corrected category? flipped escalation? edited draft text? a reason)?
- How would you actually use it — growing a labeled eval set, retrieving similar past corrections as few-shot examples, deriving rules, fine-tuning? What would you reach for first and why?
- How do you separate a reviewer rewording for tone from a reviewer correcting the classification?
- How do you avoid feedback-loop drift (amplifying one reviewer's bias) and catch regressions?
- Given the fraud-confidentiality rule: how do you make sure review data for fraud cases never teaches the model to disclose detection signals, and never lands in a context that generates customer-facing text?

## What we're assessing

- Correct, **validated structured output** and sensible control flow
- Pragmatic **prompt design** and **grounding** (no hallucinated facts/links)
- **Careful information disclosure** — does sensitive/fraud info ever leak to the customer?
- Code you'd put in a PR: structure, naming, error handling, a test or two
- How you **reason about trade-offs** — edge cases, confidence, evaluation, cost/latency
- Communication: clear thinking on a smaller result beats a black box

## What we're _not_ assessing

- A polished UI or web framework
- Perfect classification accuracy on every ticket
- Memorizing SDK syntax — look things up freely

Good luck, and please think out loud.
