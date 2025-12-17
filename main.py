from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ALLOW ONLY MARKETTOOLHUB
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://markettoolhub.com",
        "https://www.markettoolhub.com"
    ],
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type", "X-API-Key"],
)

class TradingAnswers(BaseModel):
    risk_management: str
    entry_strategy: str
    overtrading: str
    emotions: str
    stop_loss: str


@app.get("/")
def home():
    return {"message": "Trading Analyzer API is running"}


# AI-LIKE INSIGHT FUNCTION
def ai_insight(answers: dict):
    insights = []

    if answers["risk_management"] == "no":
        insights.append("Lack of risk management is increasing drawdowns.")

    if answers["overtrading"] == "yes":
        insights.append("Overtrading indicates impatience or lack of clear setup.")

    if answers["emotions"] == "yes":
        insights.append("Emotional decision-making is affecting consistency.")

    if answers["entry_strategy"] == "random":
        insights.append("Unplanned entries reduce probability of success.")

    if answers["stop_loss"] == "no":
        insights.append("Absence of stop-loss exposes capital to high risk.")

    if not insights:
        insights.append("You follow a structured trading process. Focus on consistency.")

    return insights


@app.post("/analyze")
def analyze_trading(answers: TradingAnswers):
    score = 0
    reasons = []

    if answers.risk_management == "no":
        score += 2
        reasons.append("No risk management")

    if answers.stop_loss == "no":
        score += 2
        reasons.append("No stop loss usage")

    if answers.overtrading == "yes":
        score += 1
        reasons.append("Overtrading")

    if answers.emotions == "yes":
        score += 1
        reasons.append("Emotional trading")

    if answers.entry_strategy == "random":
        score += 1
        reasons.append("No clear entry strategy")

    severity = "High" if score >= 4 else "Medium" if score >= 2 else "Low"

    # AI insights
    ai_insights = ai_insight(answers.dict())
    confidence_score = max(30, 100 - (len(ai_insights) * 12))

    return {
        "root_cause": reasons,
        "severity": severity,
        "suggestion": "Use a fixed strategy, strict stop-loss, and disciplined risk management.",
        "ai_insights": ai_insights,
        "confidence_score": confidence_score
    }
