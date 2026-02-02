from fastapi import FastAPI
from pydantic import BaseModel
from ghost_prompt_shield import GhostPromptShield, SafetyState, SafetyDecision

app = FastAPI(
    title="Ghost Prompt Shield",
    description="Hidden AI prompt safety decision layer",
    version="1.0"
)

# Single instance for demo.
# In production, state should be per-user or per-session.
shield = GhostPromptShield()
state = SafetyState()


class PromptRequest(BaseModel):
    prompt: str


class DecisionResponse(BaseModel):
    decision: str


@app.post("/check", response_model=DecisionResponse)
def check_prompt(request: PromptRequest):
    """
    Hidden safety check endpoint.
    Returns ONLY a decision.
    """
    decision = shield.evaluate(request.prompt, state)
    return {"decision": decision.value}


@app.get("/health")
def health_check():
    """
    Simple health endpoint so '/' is not confusing.
    """
    return {"status": "ok", "service": "ghost-prompt-shield"}
