"""
Optional agent integrations: Unbrowse (task/paper fetch by intent), Solana AI (payments).

See SOLANA_AI_AND_UNBROWSE.md for design and usage.
"""

from paperforge.agents.unbrowse_fetch import fetch_paper_by_intent
from paperforge.agents.solana_payout import send_consensus_payouts

__all__ = ["fetch_paper_by_intent", "send_consensus_payouts"]
