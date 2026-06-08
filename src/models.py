"""Data models for the triage agent.

These are deliberately minimal stubs. You are free to change, extend, or
replace them. They exist only to suggest a starting shape.
"""

from pydantic import BaseModel


# TODO: fill these in. Consider using enums for category / priority so the
# model's output is constrained and validated.
class TriageResult(BaseModel):
    ticket_id: str
