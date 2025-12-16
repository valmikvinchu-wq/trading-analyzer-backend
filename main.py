from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ALLOW WEBSITE TO CONNECT
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://markettoolhub.com",
        "https://www.markettoolhub.com"
    ],
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
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

    return {
        "root_cause": reasons,
        "severity": severity,
        "suggestion": "Use fixed strategy, strict stop loss, and risk management"
    }

