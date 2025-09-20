from fastapi import FastAPI, Query
from src.sentiment_agent import SentimentAgent

app = FastAPI()
sentiment_agent = SentimentAgent()

@app.get("/analyze")
async def analyze(text: str = Query(..., description="Input financial news or text")):
    result = sentiment_agent.analyze(text)
    return {"text": text, "sentiment": result}
