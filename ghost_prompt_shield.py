from enum import Enum
from typing import List


class SafetyDecision(Enum):
    ALLOW = "ALLOW"
    WARN = "WARN"
    BLOCK = "BLOCK"


class SafetyState:
    def __init__(self):
        self.risk_score: int = 0
        self.history: List[str] = []


class GhostPromptShield:
    def __init__(self):
        self.override_phrases = [
            "ignore previous instructions",
            "reveal system prompt",
            "bypass safety",
            "disable safety",
            "developer mode",
            "jailbreak"
        ]

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

        self.soft_markers = [
            "hypothetically",
            "just curious",
            "for educational purposes",
            "purely theoretical"
        ]

    def evaluate(self, prompt: str, state: SafetyState) -> SafetyDecision:
        text = prompt.lower().strip()
        risk_delta = 0

        # Hard block
        for phrase in self.override_phrases:
            if phrase in text:
                state.risk_score = 100
                state.history.append(prompt)
                return SafetyDecision.BLOCK

        # Role impersonation
        if (
            any(t in text for t in self.role_triggers)
            and any(r in text for r in self.privileged_roles)
        ):
            risk_delta += 40

        # Soft manipulation
        if any(m in text for m in self.soft_markers):
            risk_delta += 10

        # Escalation
        if state.risk_score > 30 and any(t in text for t in self.role_triggers):
            risk_delta += 20

        state.risk_score += risk_delta
        state.history.append(prompt)

        if risk_delta == 0 and state.risk_score > 0:
            state.risk_score = max(0, state.risk_score - 10)

        if state.risk_score >= 70:
            return SafetyDecision.BLOCK

        if state.risk_score >= 30:
            return SafetyDecision.WARN

        return SafetyDecision.ALLOW
