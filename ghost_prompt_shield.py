from enum import Enum
from typing import List


class SafetyDecision(Enum):
    ALLOW = "ALLOW"
    WARN = "WARN"
    BLOCK = "BLOCK"


class SafetyState:
    """
    Per-session / per-user safety memory.
    In production, this would be stored per user or request context.
    """
    def __init__(self):
        self.risk_score: int = 0
        self.history: List[str] = []


class GhostPromptShield:
    """
    Hidden prompt safety decision engine.
    This class NEVER talks to users directly.
    """

    def __init__(self):
        # Hard system override attempts (instant block)
        self.hard_block_phrases = [
            "ignore previous instructions",
            "reveal system prompt",
            "show system prompt",
            "bypass safety",
            "disable safety",
            "developer mode",
            "jailbreak"
        ]

        # Role / authority escalation
        self.role_triggers = [
            "act as",
            "pretend to be",
            "you are now",
            "assume the role of"
        ]

        self.privileged_roles = [
            "system",
            "developer",
            "admin",
            "administrator",
            "root"
        ]

        # Soft manipulation markers
        self.soft_markers = [
            "just for learning",
            "educational purposes",
            "hypothetically",
            "purely theoretical",
            "just curious"
        ]

        # Clearly benign / educational patterns
        self.benign_starters = [
            "what is",
            "define",
            "explain",
            "how does",
            "why does",
            "tell me about"
        ]

    def evaluate(self, prompt: str, state: SafetyState) -> SafetyDecision:
        text = prompt.lower().strip()
        risk_delta = 0

        # -------------------------------------------------
        # 1. Immediate hard block (non-negotiable)
        # -------------------------------------------------
        for phrase in self.hard_block_phrases:
            if phrase in text:
                state.risk_score = 100
                state.history.append(prompt)
                return SafetyDecision.BLOCK

        # -------------------------------------------------
        # 2. Benign informational override (UX fix)
        # -------------------------------------------------
        if any(text.startswith(b) for b in self.benign_starters):
            # Strong trust recovery for clean educational queries
            state.risk_score = max(0, state.risk_score - 30)
            state.history.append(prompt)
            return SafetyDecision.ALLOW

        # -------------------------------------------------
        # 3. Role impersonation / authority escalation
        # -------------------------------------------------
        if (
            any(t in text for t in self.role_triggers)
            and any(r in text for r in self.privileged_roles)
        ):
            risk_delta += 40

        # -------------------------------------------------
        # 4. Soft manipulation / probing language
        # -------------------------------------------------
        if any(m in text for m in self.soft_markers):
            risk_delta += 10

        # -------------------------------------------------
        # 5. Escalation across turns
        # -------------------------------------------------
        if state.risk_score > 30 and any(t in text for t in self.role_triggers):
            risk_delta += 20

        # -------------------------------------------------
        # 6. Update state
        # -------------------------------------------------
        state.risk_score = min(100, state.risk_score + risk_delta)
        state.history.append(prompt)

        # -------------------------------------------------
        # 7. Risk decay (trust recovery over time)
        # -------------------------------------------------
        if risk_delta == 0:
            state.risk_score = max(0, state.risk_score - 20)

        # -------------------------------------------------
        # 8. Final decision
        # -------------------------------------------------
        if state.risk_score >= 70:
            return SafetyDecision.BLOCK

        if state.risk_score >= 30:
            return SafetyDecision.WARN

        return SafetyDecision.ALLOW
