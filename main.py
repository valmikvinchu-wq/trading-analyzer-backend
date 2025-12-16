from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ------------------------
# Data model (what user sends)
# ------------------------
class TradingAnswers(BaseModel):
    risk_management: str
    entry_strategy: str
    overtrading: str
    emotions: str
    stop_loss: str


# ------------------------
# Home test
# ------------------------
@app.get("/")
def home():
    return {"message": "Trading Analyzer API is running"}


# ------------------------
# Analyze endpoint
# ------------------------
@app.post("/analyze")
def analyze_trading(answers: TradingAnswers):

    score = 0
    reasons = []

    if answers.risk_management.lower() == "no":
        score += 2
        reasons.append("No risk management")

    if answers.stop_loss.lower() == "no":
        score += 2
        reasons.append("No stop loss usage")

    if answers.overtrading.lower() == "yes":
        score += 1
        reasons.append("Overtrading")

    if answers.emotions.lower() == "yes":
        score += 1
        reasons.append("Emotional trading")

    if answers.entry_strategy.lower() == "random":
        score += 1
        reasons.append("No clear entry strategy")

    if score >= 4:
        severity = "High"
    elif score >= 2:
        severity = "Medium"
    else:
        severity = "Low"

    return {
        "root_cause": reasons,
        "severity": severity,
        "suggestion": "Follow a fixed strategy, strict stop loss, and proper risk management"
    }